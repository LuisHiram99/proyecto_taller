from sqlalchemy import Column, ForeignKey, Integer, String, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from .database import Base
import enum


class RoleEnum(enum.Enum):
    admin = "admin"
    manager = "manager"
    worker = "worker"


class StatusEnum(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Workshop(Base):
    __tablename__ = "workshops"

    workshop_id = Column(Integer, primary_key=True, index=True)
    workshop_name = Column(String(100), nullable=False)
    address = Column(String(200))
    opening_hours = Column(String(20))
    closing_hours = Column(String(20))


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String(20), nullable=False)
    updated_at = Column(String(20), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String)
    workshop_id = Column(Integer, ForeignKey("workshops.workshop_id"), nullable=False)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100))
    role = Column(
        PGEnum(RoleEnum, name="role_enum", create_type=False),
        nullable=False,
    )
    hashed_password = Column(String(100), nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.workshop_id"), nullable=False, default=1)


class Worker(Base):
    __tablename__ = "workers"

    worker_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    position = Column(String(100), nullable=False)
    nickname = Column(String(50))
    workshop_id = Column(Integer, ForeignKey("workshops.workshop_id"), nullable=False)


class Car(Base):
    __tablename__ = "cars"

    car_id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class CustomerCar(Base):
    __tablename__ = "customer_car"

    customer_car_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.car_id"), nullable=False)
    license_plate = Column(String(20), nullable=False)
    color = Column(String(50))


class Part(Base):
    __tablename__ = "parts"

    part_id = Column(Integer, primary_key=True, index=True)
    part_name = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    description = Column(String(255))
    category = Column(String(100))


class PartWorkshop(Base):
    __tablename__ = "part_workshop"

    part_id = Column(Integer, ForeignKey("parts.part_id"), nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.workshop_id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    purchase_price = Column(Integer, nullable=False)
    sale_price = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("part_id", "workshop_id", name="part_workshop_pk"),
    )


class PartCar(Base):
    __tablename__ = "part_car"

    car_id = Column(Integer, ForeignKey("cars.car_id"), nullable=False)
    part_id = Column(Integer, ForeignKey("parts.part_id"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("car_id", "part_id", name="car_parts_pk"),
    )


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    workshop_id = Column(Integer, ForeignKey("workshops.workshop_id"), nullable=False)
    customer_car_id = Column(Integer, ForeignKey("customer_car.customer_car_id"), nullable=False)

    invoice = Column(String(100), nullable=False)
    service_description = Column(String(255))
    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20))
    status = Column(
        PGEnum(StatusEnum, name="status_enum", create_type=True),
        nullable=False,
    )


class JobParts(Base):
    __tablename__ = "job_parts"

    job_id = Column(Integer, ForeignKey("jobs.job_id"), nullable=False)
    part_id = Column(Integer, ForeignKey("parts.part_id"), nullable=False)
    quantity_used = Column(Integer, default=1)

    __table_args__ = (
        PrimaryKeyConstraint("job_id", "part_id", name="job_parts_pk"),
    )


class JobWorkers(Base):
    __tablename__ = "job_workers"

    job_id = Column(Integer, ForeignKey("jobs.job_id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("workers.worker_id"), nullable=False)
    job_role = Column(String(100), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("job_id", "worker_id", name="job_workers_pk"),
    )