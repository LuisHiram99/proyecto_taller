from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Annotated
from auth.auth import get_current_user, is_admin

from db import models, schemas, database
from db.database import get_db

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/customer_car/", response_model=schemas.CustomerCar)
async def create_customer_car(current_user: user_dependency, customer_car: schemas.CustomerCarCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new customer_car
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    customer_res = await db.execute(select(models.Customer).where(models.Customer.customer_id == customer_car.customer_id))
    if customer_res.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    car_res = await db.execute(select(models.Car).where(models.Car.car_id == customer_car.car_id))
    if car_res.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Car not found")

    db_customer_car = models.CustomerCar(**customer_car.model_dump())
    db.add(db_customer_car)
    await db.commit()
    await db.refresh(db_customer_car)
    return db_customer_car

@router.get("/customer_car/", response_model=List[schemas.CustomerCar])
async def read_customers_cars(current_user: user_dependency, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all customers_cars with pagination
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    result = await db.execute(
        select(models.CustomerCar).offset(skip).limit(limit)
    )
    customers_cars = result.scalars().all()
    return customers_cars


@router.get("/customer_car/{customer_car_id}", response_model=schemas.CustomerCar)
async def read_customer_car(current_user: user_dependency, customer_car_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific customer_car by ID
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    result = await db.execute(
        select(models.CustomerCar).filter(models.CustomerCar.customer_car_id == customer_car_id)
    )
    db_customer_car = result.scalar_one_or_none()
    if db_customer_car is None:
        raise HTTPException(status_code=404, detail="CustomerCar not found")
    return db_customer_car

@router.put("/customer_car/{customer_car_id}", response_model=schemas.CustomerCar)
async def update_customer_car(current_user: user_dependency, customer_car_id: int, customer_car: schemas.CustomerCarUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update an existing customer_car (partial updates allowed)
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    result = await db.execute(
        select(models.CustomerCar).where(models.CustomerCar.customer_car_id == customer_car_id)
    )
    db_customer_car = result.scalar_one_or_none()
    if db_customer_car is None:
        raise HTTPException(status_code=404, detail="CustomerCar not found")

    # Only update fields that are provided in the request
    customer_data = customer_car.model_dump(exclude_unset=True)

    if "customer_id" in customer_data:
        customer_res = await db.execute(select(models.Customer).where(models.Customer.customer_id == customer_data["customer_id"]))
        if customer_res.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Customer not found")

    if "car_id" in customer_data:
        car_res = await db.execute(select(models.Car).where(models.Car.car_id == customer_data["car_id"]))
        if car_res.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Car not found")

    for key, value in customer_data.items():
        setattr(db_customer_car, key, value)

    await db.commit()
    await db.refresh(db_customer_car)
    return db_customer_car

@router.delete("/customer_car/{customer_car_id}", response_model=schemas.CustomerCar)
async def delete_customer_car(current_user: user_dependency, customer_car_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a customer_car
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    result = await db.execute(
        select(models.CustomerCar).filter(models.CustomerCar.customer_car_id == customer_car_id)
    )
    db_customer_car = result.scalar_one_or_none()
    if db_customer_car is None:
        raise HTTPException(status_code=404, detail="CustomerCar not found")

    await db.execute(
        delete(models.CustomerCar).where(models.CustomerCar.customer_car_id == customer_car_id)
    )
    await db.commit()
    return db_customer_car
