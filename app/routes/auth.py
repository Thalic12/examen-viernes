from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from pydantic import BaseModel, EmailStr
from fastapi import BackgroundTasks
# Importamos la lógica corregida de los servicios
from ..services.auth_service import register_user, verify_user_otp, login_user, resend_otp

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


class ResendOtp(BaseModel):
    email: EmailStr

# --- ENDPOINTS ---

from fastapi import BackgroundTasks # Importa esto

@router.post("/register")
def register(data: Register, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Crea el usuario y delega el envío del OTP a una tarea en segundo plano.
    """
    # Pasamos background_tasks a la función lógica
    return register_user(data, db, background_tasks)
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


@router.post("/resend-otp")
def resend_code(data: ResendOtp, db: Session = Depends(get_db)):
    return resend_otp(data, db)