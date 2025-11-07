from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Annotated
from auth.auth import get_current_user, is_admin, admin_required
from . import service

from db import models, schemas, database
from db.database import get_db

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

# ---------------- All cars endpoints ----------------

@router.post("/cars/", response_model=schemas.Car)
async def create_car(
    car: schemas.CarCreate, 
    current_user: dict = Depends(admin_required),
    db: AsyncSession = Depends(get_db)):
    """
    Create a new car
    """
    # Await the async service function
    return await service.create_car(car, db, current_user)

@router.get("/cars/", response_model=List[schemas.Car])
async def read_cars(
    current_user: dict = Depends(admin_required), 
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)):
    """
    Get all cars with pagination
    """
    return await service.get_all_cars(current_user, db, skip, limit)


@router.get("/cars/{car_id}", response_model=schemas.Car)
async def read_car(
    car_id: int,
    current_user: dict = Depends(admin_required), 
    db: AsyncSession = Depends(get_db),
    ):
    """
    Get a specific car by ID
    """
    # if the current user is not admin, raise 403
    # Fix parameter order to match service signature
    return await service.get_car_by_id(current_user, db, car_id)

@router.put("/cars/{car_id}", response_model=schemas.Car)
async def update_car( 
    car_id: int, 
    car: schemas.CarUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(admin_required)):
    """
    Update an existing car (partial updates allowed)
    """
    return await service.update_car(current_user, car_id, db, car)

@router.delete("/cars/{car_id}", response_model=schemas.Car)
async def delete_car(
    car_id: int, 
    current_user: dict = Depends(admin_required), 
    db: AsyncSession = Depends(get_db)):
    """
    Delete a car
    """
    return await service.delete_car(current_user, db, car_id)