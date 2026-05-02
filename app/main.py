from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

from .database import engine, Base
# MODELOS (Asegúrate de que estas rutas sean correctas según tu estructura)
from app.models import student_model, user 

# ROUTES
from .routes import student, auth 

# MIDDLEWARES
from .middleware.logging_middleware import LoggingMiddleware
from .middleware.rate_limit_middleware import RateLimitMiddleware
from .middleware.audit_middleware import AuditMiddleware

# CREAR TABLAS
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CONFIGURACIÓN DE CARPETAS ---
BASE_DIR = Path(__file__).resolve().parent
# Si main.py está dentro de una carpeta 'app', BASE_DIR.parent apunta a la raíz del proyecto
FRONTEND_DIR = BASE_DIR.parent / "frontend"

# --- MIDDLEWARES ---
# Nota: Se ejecutan en orden inverso al que se añaden. 
# CORS suele ir primero para evitar bloqueos de navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware) # Movido arriba para proteger antes de procesar
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuditMiddleware)

# --- ARCHIVOS ESTÁTICOS ---
# Importante: Montar antes de las rutas de redirección si es posible
if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")
else:
    print(f"ADVERTENCIA: No se encontró la carpeta frontend en {FRONTEND_DIR}")

# --- REDIRECCIONES ---

@app.get("/", include_in_schema=False)
def root():
    # Redirigimos directamente al archivo físico dentro del mount de estáticos
    return RedirectResponse(url="/frontend/login.html")

@app.get("/index", include_in_schema=False)
def index():
    return RedirectResponse(url="/frontend/index.html")

@app.get("/verify", include_in_schema=False)
def verify():
    return RedirectResponse(url="/frontend/auth.html")

@app.get("/registro", include_in_schema=False)
def registro():
    return RedirectResponse(url="/frontend/registro.html")

# --- ROUTES API ---
app.include_router(student.router)
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(auth.router)  