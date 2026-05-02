from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

# Importar tus componentes (asegúrate de que los nombres coincidan)
from app.database import engine, Base
from .routes import student, auth 
from .middleware.logging_middleware import LoggingMiddleware
from .middleware.rate_limit_middleware import RateLimitMiddleware
from .middleware.audit_middleware import AuditMiddleware

# CREAR TABLAS (Crucial para que Render cree el .db al arrancar)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CONFIGURACIÓN DE CARPETAS ---
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

# --- MIDDLEWARES ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuditMiddleware)

# --- ARCHIVOS ESTÁTICOS ---
if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")
else:
    print(f"ERROR: No se encontró la carpeta frontend en {FRONTEND_DIR}")

# --- RUTAS DE NAVEGACIÓN (Corregidas) ---
@app.get("/", include_in_schema=False)
def root():
    # Servimos el login directamente en la raíz
    return FileResponse(str(FRONTEND_DIR / "login.html"))

@app.get("/index", include_in_schema=False)
def index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/registro", include_in_schema=False)
def registro():
    return FileResponse(str(FRONTEND_DIR / "registro.html"))

# --- ROUTES API (Sin duplicados) ---
app.include_router(student.router, prefix="/students", tags=["Students"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])