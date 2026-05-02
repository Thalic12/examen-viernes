from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class OTP(Base):
    __tablename__ = "otp_codes"  # Nombre consistente

    id = Column(Integer, primary_key=True, index=True)

    # Correo asociado al código
    email = Column(String, index=True)

    # Código de 6 dígitos
    code = Column(String)

    # Fecha de expiración
    expires_at = Column(DateTime)

    # Fecha de creación
    created_at = Column(DateTime, default=datetime.utcnow)