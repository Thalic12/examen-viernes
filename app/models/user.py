# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from ..database import Base
import datetime

# 👤 MODELO DE USUARIO (tabla users)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # ✅ ESTA ES LA QUE FALTABA:
    # Se usa para habilitar/deshabilitar la cuenta tras el login
    is_active = Column(Boolean, default=False) 

    # 🔐 Indica si el usuario ya verificó OTP (puedes usar esta o is_active)
    is_verified = Column(Boolean, default=False)

    # ⏳ Guarda la última vez que verificó (para control de 3 días)
    last_verification = Column(DateTime, nullable=True)


# 🔐 MODELO OTP (códigos temporales)
class OTP(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    code = Column(String)
    expires_at = Column(DateTime)