from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Annotated
from auth.auth import get_current_user, admin_required
from . import service
from ..rate_limiter import limiter

from db import models, schemas, database
from db.database import get_db

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/customer_car/", response_model=schemas.CustomerCar)
@limiter.limit("10/minute")
async def create_customer_car(
    request: Request,
    customer_car: schemas.CustomerCarCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(admin_required)):
    """
    Create a new customer_car
    """
    # Pass arguments in the order expected by the service: (customer_car, db, current_user)
    return await service.create_customer_car(customer_car, db, current_user)

@router.get("/customer_car/", response_model=List[schemas.CustomerCar])
@limiter.limit("10/minute")
async def read_customers_cars(
    request: Request,
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(admin_required),
    skip: int = 0, 
    limit: int = 100):
    """
    Get all customers_cars with pagination
    """
    return await service.get_all_customers_cars(db, current_user, skip, limit)


@router.get("/customer_car/{customer_car_id}", response_model=schemas.CustomerCar)
@limiter.limit("10/minute")
async def read_customer_car(
    request: Request,
    customer_car_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(admin_required)):
    """
    Get a specific customer_car by ID
    """
    return await service.get_customer_car_by_id(customer_car_id, db, current_user)

@router.put("/customer_car/{customer_car_id}", response_model=schemas.CustomerCar)
@limiter.limit("10/minute")
async def update_customer_car(
    request: Request,
    customer_car_id: int,
    customer_car_update: schemas.CustomerCarUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(admin_required)):
    """
    Update an existing customer_car (partial updates allowed)
    """
    return await service.update_customer_car(customer_car_id, customer_car_update, db, current_user)

@router.delete("/customer_car/{customer_car_id}", response_model=schemas.CustomerCar)
@limiter.limit("10/minute")
async def delete_customer_car(
    request: Request,
    customer_car_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(admin_required)):
    """
    Delete a customer_car
    """
    return await service.delete_customer_car(customer_car_id, db, current_user)
