from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from pydantic import BaseModel, EmailStr

# Importamos la lógica corregida de los servicios
from ..services.auth_service import register_user, verify_user_otp, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

# --- ESQUEMAS DE VALIDACIÓN (Pydantic) ---

class Register(BaseModel):
    name: str
    email: EmailStr # Valida que sea un correo real
    password: str

class Login(BaseModel):
    email: EmailStr
    password: str

class Verify(BaseModel):
    email: EmailStr
    code: str # El código de 6 dígitos

# --- ENDPOINTS ---

@router.post("/register")
def register(data: Register, db: Session = Depends(get_db)):
    """
    Crea el usuario y envía el OTP inmediatamente.
    Expira en 5 minutos.
    """
    return register_user(data, db)

@router.post("/verify")
def verify(data: Verify, db: Session = Depends(get_db)):
    """
    Valida el código y devuelve el TOKEN de 3 días.
    Si es exitoso, el frontend lo manda al CRUD.
    """
    # Usamos la función corregida del service
    return verify_user_otp(data, db)

@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    """
    Para usuarios que ya tienen cuenta. 
    Les envía un nuevo código OTP al correo.
    """
    return login_user(data, db)