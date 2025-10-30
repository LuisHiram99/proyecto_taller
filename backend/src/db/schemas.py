from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    worker = "worker"


# Base Pydantic Models (For Create/Update operations)
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: Optional[str] = None
    workshop_id: int


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    role: RoleEnum
    workshop_id: int


class CarBase(BaseModel):
    year: int
    brand: str
    model: str


class CustomerCarBase(BaseModel):
    customer_id: int
    car_id: int
    license_plate: str
    color: Optional[str] = None


# Models for responses (including IDs)
class Customer(CustomerBase):
    customer_id: int

    model_config = {"from_attributes": True}


class User(UserBase):
    user_id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {"example": {
            "user_id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "role": "admin",
            "workshop_id": 1
        }}
    }


class Car(CarBase):
    car_id: int

    model_config = {"from_attributes": True}


class CustomerCar(CustomerCarBase):
    customer_car_id: int

    model_config = {"from_attributes": True}


# Models for creating new records
class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    workshop_id: Optional[int] = None


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    password: str  # plain password for creation; will be hashed in the handler
    role: RoleEnum
    workshop_id: int

    model_config = {"json_schema_extra": {"example": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "secretpassword",
        "role": "admin",
        "workshop_id": 1
    }}}


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None
    workshop_id: Optional[int] = None


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    year: Optional[int] = None
    brand: Optional[str] = None
    model: Optional[str] = None


class CustomerCarCreate(CustomerCarBase):
    pass


class CustomerCarUpdate(CustomerCarBase):
    pass


class WorkshopBase(BaseModel):
    workshop_name: str
    address: Optional[str] = None
    opening_hours: Optional[str] = None
    closing_hours: Optional[str] = None


class Workshop(WorkshopBase):
    workshop_id: int

    model_config = {"from_attributes": True}


class WorkshopCreate(WorkshopBase):
    pass


class WorkshopUpdate(BaseModel):
    workshop_name: Optional[str] = None
    address: Optional[str] = None
    opening_hours: Optional[str] = None
    closing_hours: Optional[str] = None