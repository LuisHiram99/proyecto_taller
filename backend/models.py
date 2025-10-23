from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

class RolEnum(enum.Enum):
    admin = "admin"
    gerente = "gerente"
    trabajador = "trabajador"

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    rol = Column(Enum(RolEnum), nullable=False)
    acronimo = Column(String(50))