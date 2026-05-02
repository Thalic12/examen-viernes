import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.user import OTP

def generate_code():
    # Genera un string de 6 números
    return str(random.randint(100000, 999999))

def create_otp_record(email: str, db: Session):
    # Eliminar códigos viejos si existen para limpiar la BD
    db.query(OTP).filter(OTP.email == email).delete()
    
    code = generate_code()
    # Expiración en 5 minutos exactos
    expires = datetime.utcnow() + timedelta(minutes=5)
    
    new_otp = OTP(
        email=email,
        code=code,
        expires_at=expires
    )
    
    db.add(new_otp)
    # No hacemos commit aquí para que auth_service maneje la transacción completa
    return code