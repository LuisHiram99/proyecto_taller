from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from .database import Base
import enum

class RolEnum(enum.Enum):
    admin = "admin"
    gerente = "gerente"
    trabajador = "trabajador"

class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String)
    
    carros = relationship("ClienteCarro", back_populates="cliente")

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    # Use the existing Postgres enum type name 'rol_enum' and do not attempt
    # to create it from SQLAlchemy (create_type=False) to avoid type name
    # mismatches with the DB.
    rol = Column(
        PGEnum(RolEnum, name="rol_enum", create_type=False),
        nullable=False,
    )
    acronimo = Column(String(50), nullable=False)

class Carro(Base):
    __tablename__ = "carros"

    carro_id = Column(Integer, primary_key=True, index=True)
    año = Column(Integer, nullable=False)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    
    clientes = relationship("ClienteCarro", back_populates="carro")

class ClienteCarro(Base):
    __tablename__ = "cliente_carro"

    cliente_carro_id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.cliente_id"), nullable=False)
    carro_id = Column(Integer, ForeignKey("carros.carro_id"), nullable=False)
    placas = Column(String(20), nullable=False)
    color = Column(String(50))
    
    cliente = relationship("Cliente", back_populates="carros")
    carro = relationship("Carro", back_populates="clientes")