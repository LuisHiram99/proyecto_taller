from sqlalchemy import Column, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from .database import Base
import enum

class RolEnum(enum.Enum):
    admin = "admin"
    gerente = "gerente"
    trabajador = "trabajador"

class EstadoEnum(enum.Enum):
    pendiente = "pendiente"
    en_proceso = "en_proceso"
    completado = "completado"

class Taller(Base):
    __tablename__ = "talleres"

    taller_id = Column(Integer, primary_key=True, index=True)
    nombre_taller = Column(String(100), nullable=False)
    direccion = Column(String(200))
    horario_apertura = Column(String(20))
    horario_cierre = Column(String(20))

    piezas = relationship("PiezaTaller", back_populates="taller")
    usuarios = relationship("Usuario", back_populates="taller")
    clientes = relationship("Cliente", back_populates="taller")


class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String)
    taller_id = Column(Integer, ForeignKey("talleres.taller_id"), nullable=False)

    taller = relationship("Taller", back_populates="clientes")
    carros = relationship("ClienteCarro", back_populates="cliente")

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20))
    correo = Column(String(100))
    rol = Column(
        PGEnum(RolEnum, name="rol_enum", create_type=False),
        nullable=False,
    )
    pseudonimo = Column(String(50))
    hashpassword = Column(String(60), nullable=False)  # <- contraseña hashed
    taller_id = Column(Integer, ForeignKey("talleres.taller_id"), nullable=False)

    taller = relationship("Taller", back_populates="usuarios")
    trabajos = relationship("TrabajoUsuarios", back_populates="usuario")

class Carro(Base):
    __tablename__ = "carros"

    carro_id = Column(Integer, primary_key=True, index=True)
    año = Column(Integer, nullable=False)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    
    clientes = relationship("ClienteCarro", back_populates="carro")
    piezas = relationship("PiezaCarro", back_populates="carro")

class ClienteCarro(Base):
    __tablename__ = "cliente_carro"

    cliente_carro_id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.cliente_id"), nullable=False)
    carro_id = Column(Integer, ForeignKey("carros.carro_id"), nullable=False)
    placas = Column(String(20), nullable=False)
    color = Column(String(50))
    
    
    cliente = relationship("Cliente", back_populates="carros")
    carro = relationship("Carro", back_populates="clientes")

class Pieza(Base):
    __tablename__ = "piezas"

    pieza_id = Column(Integer, primary_key=True, index=True)
    nombre_pieza = Column(String(100), nullable=False)
    marca = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    categoria = Column(String(100))

    taller = relationship("PiezaTaller", back_populates="pieza")
    trabajo = relationship("TrabajoPiezas", back_populates="pieza")
    carro = relationship("PiezaCarro", back_populates="pieza")

class PiezaTaller(Base):
    __tablename__ = "pieza_taller"

    pieza_id = Column(Integer, ForeignKey("piezas.pieza_id"), nullable=False)
    taller_id = Column(Integer, ForeignKey("talleres.taller_id"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_compra = Column(Integer, nullable=False)
    precio_venta = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('pieza_id', 'taller_id', name='pieza_taller_pk'),
    )

    piezas_taller = relationship("PiezaTaller", back_populates="pieza")
    taller = relationship("Taller", back_populates="piezas")

class PiezaCarro(Base):
    __tablename__ = "pieza_carro"

    carro_id = Column(Integer, ForeignKey("carros.carro_id"), nullable=False)
    pieza_id = Column(Integer, ForeignKey("piezas.pieza_id"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('carro_id', 'pieza_id', name='carro_piezas_pk'),
    )

    pieza = relationship("Pieza", back_populates="carro")
    carro = relationship("Carro", back_populates="piezas")

class Trabajo(Base):
    __tablename__ = "trabajos"

    trabajo_id = Column(Integer, primary_key=True, index=True)
    taller_id = Column(Integer, ForeignKey("talleres.taller_id"), nullable=False)
    cliente_carro_id = Column(Integer, ForeignKey("cliente_carro.cliente_carro_id"), nullable=False)

    facturo = Column(String(100), nullable=False)
    descripcion_servicio = Column(String(255))
    fecha_inicio = Column(String(20), nullable=False)
    fecha_fin = Column(String(20))
    estado = Column(
        PGEnum(EstadoEnum, name="estado_enum", create_type=True),
        nullable=False,
    )

    cliente_carro = relationship("ClienteCarro")
    taller = relationship("Taller")
    piezas = relationship("TrabajoPiezas", back_populates="trabajo")

class TrabajoPiezas(Base):
    __tablename__ = "trabajo_piezas"

    trabajo_id = Column(Integer, ForeignKey("trabajos.trabajo_id"), nullable=False)
    pieza_id = Column(Integer, ForeignKey("piezas.pieza_id"), nullable=False)
    cantidad_usada = Column(Integer, default=1)

    __table_args__ = (
        PrimaryKeyConstraint('trabajo_id', 'pieza_id', name='trabajo_piezas_pk'),
    )

    piezas = relationship("Pieza", back_populates="trabajo")
    trabajo = relationship("Trabajo", back_populates="piezas")

class TrabajoUsuarios(Base):
    __tablename__ = "trabajo_usuarios"

    trabajo_id = Column(Integer, ForeignKey("trabajos.trabajo_id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    rol_trabajo = Column(String(100), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('trabajo_id', 'usuario_id', name='trabajo_usuarios_pk'),
    )

    trabajo = relationship("Trabajo", back_populates="usuarios")
    usuario = relationship("Usuario", back_populates="trabajos")


