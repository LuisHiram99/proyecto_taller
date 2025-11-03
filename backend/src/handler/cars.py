from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Annotated
from auth.auth import get_current_user, is_admin


from db import models, schemas, database
from db.database import get_db

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

# ---------------- All cars endpoints ----------------

@router.post("/cars/", response_model=schemas.Car)
async def create_car(current_user: user_dependency, car: schemas.CarCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new car
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    db_car = models.Car(**car.model_dump())
    db.add(db_car)
    await db.commit()
    await db.refresh(db_car)
    return db_car

@router.get("/cars/", response_model=List[schemas.Car])
async def read_cars(current_user: user_dependency, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all cars with pagination
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    result = await db.execute(
        select(models.Car).offset(skip).limit(limit)
    )
    cars = result.scalars().all()
    return cars


@router.get("/cars/{car_id}", response_model=schemas.Car)
async def read_car(current_user: user_dependency, car_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific car by ID
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    result = await db.execute(
        select(models.Car).filter(models.Car.car_id == car_id)
    )
    db_car = result.scalar_one_or_none()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

@router.put("/cars/{car_id}", response_model=schemas.Car)
async def update_car(current_user: user_dependency, car_id: int, car: schemas.CarUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update an existing car (partial updates allowed)
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    result = await db.execute(
        select(models.Car).where(models.Car.car_id == car_id)
    )
    db_car = result.scalar_one_or_none()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    # Only update fields that are provided in the request
    car_data = car.model_dump(exclude_unset=True)
    for key, value in car_data.items():
        setattr(db_car, key, value)

    await db.commit()
    await db.refresh(db_car)
    return db_car

@router.delete("/cars/{car_id}", response_model=schemas.Car)
async def delete_car(current_user: user_dependency, car_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a car
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    result = await db.execute(
        select(models.Car).filter(models.Car.car_id == car_id)
    )
    db_car = result.scalar_one_or_none()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    await db.execute(
        delete(models.Car).where(models.Car.car_id == car_id)
    )
    await db.commit()
    return db_car
