from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum

class RolEnum(str, Enum):
    admin = "admin"
    gerente = "gerente"
    trabajador = "trabajador"

# Base Pydantic Models (For Create/Update operations)
class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    correo: Optional[str] = None

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    rol: RolEnum
    acronimo: str

class CarroBase(BaseModel):
    año: int
    marca: str
    modelo: str

class ClienteCarroBase(BaseModel):
    cliente_id: int
    carro_id: int
    placas: str
    color: Optional[str] = None

# Models for responses (including IDs)
class Cliente(ClienteBase):
    cliente_id: int
    
    # Pydantic v2: allow building model from ORM/attribute access
    model_config = {"from_attributes": True}

class Usuario(UsuarioBase):
    usuario_id: int
    
    model_config = {"from_attributes": True}

class Carro(CarroBase):
    carro_id: int
    
    model_config = {"from_attributes": True}

class ClienteCarro(ClienteCarroBase):
    cliente_carro_id: int
    
    model_config = {"from_attributes": True}

# Models for creating new records
class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    pass

class CarroCreate(CarroBase):
    pass

class CarroUpdate(BaseModel):
    año: Optional[int] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None

class ClienteCarroCreate(ClienteCarroBase):
    pass