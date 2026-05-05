import os
import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

# Carga de variables de entorno
load_dotenv()

# Variables de entorno para servicios externos
#email_user = os.getenv("EMAIL_USER")
#email_pass = os.getenv("EMAIL_PASS")

# Importaciones locales
from ..models.user import User, OTP
from .email_service import send_email
from .otp_service import create_otp_record

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_para_jwt") 
ALGORITHM = "HS256"

# --- FUNCIONES DE SEGURIDAD (Bcrypt Directo) ---

def hash_password(password: str) -> str:
    """
    Convierte la contraseña en un hash seguro.
    Truncamos a 72 caracteres para evitar errores de Bcrypt.
    """
    # Preparar la contraseña (bytes + truncado)
    pwd_bytes = password.encode('utf-8')[:72]
    # Generar salt y hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña ingresada coincide con el hash de la DB.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8')[:72], 
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    # Sesión de 3 días
    expire = datetime.utcnow() + timedelta(days=3)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- FLUJO DE REGISTRO ---

def register_user(data, db: Session):
    user_exists = db.query(User).filter(User.email == data.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Crear usuario (is_active=False hasta que valide el OTP)
    new_user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        is_active=False 
    )
    db.add(new_user)
    
    # Generar OTP y enviarlo inmediatamente
    code = create_otp_record(data.email, db)
    send_email(data.email, code)
    
    db.commit()
    return {"msg": "Usuario registrado. Por favor verifica tu correo."}

# --- FLUJO DE VERIFICACIÓN ---

def verify_user_otp(data, db: Session):
    # Buscar el OTP en la base de datos
    otp_record = db.query(OTP).filter(
        OTP.email == data.email, 
        OTP.code == data.code
    ).first()
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="Código inválido")
    
    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="El código ha expirado (5 min)")

    # Activar al usuario
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    user.is_active = True

    # Limpiar OTP usado
    db.delete(otp_record)
    db.commit()

    # Generar el token que dura 3 días
    token = create_access_token(data={"sub": user.email})
    return {
        "access_token": token, 
        "token_type": "bearer",
        "msg": "Verificación exitosa. Bienvenida/o al sistema."
    }

# --- FLUJO DE LOGIN ---

def login_user(data, db: Session):
    # 1. Buscar si el usuario existe
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    # 2. Validar la contraseña
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    # 3. Si la cuenta no está activa, reenviamos OTP para completar verificación
    if not user.is_active:
        code = create_otp_record(user.email, db)
        send_email(user.email, code)
        db.commit()
        return {
            "requires_verification": True,
            "msg": "Cuenta sin verificar. Te enviamos un nuevo código al correo."
        }

    # 4. Generar el token de acceso (3 días)
    token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": token, 
        "token_type": "bearer",
        "msg": "Sesión iniciada correctamente"
    }


def resend_otp(data, db: Session):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    code = create_otp_record(user.email, db)
    send_email(user.email, code)
    db.commit()
    return {"msg": "Nuevo código enviado al correo"}