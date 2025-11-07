from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from db import models, schemas
from exceptions.exceptions import notFoundException, fetchErrorException


# ---------------- All customer_car functions ----------------
async def create_customer_car(
        customer_car: schemas.CustomerCarCreate,
        db: AsyncSession,
        current_user: dict):
    '''
    Construct a query to create a new customer_car
    '''
    try:
        # Check if customer exist in db
        customer_res = await db.execute(select(models.Customer).where(models.Customer.customer_id == customer_car.customer_id))
        if customer_res.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Check if car exist in db
        car_res = await db.execute(select(models.Car).where(models.Car.car_id == customer_car.car_id))
        if car_res.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Car not found")

        db_customer_car = models.CustomerCar(**customer_car.model_dump())

        db.add(db_customer_car)
        await db.commit()
        await db.refresh(db_customer_car)
        return db_customer_car
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in create_customer_car: {e}")
        raise fetchErrorException
    
async def get_all_customers_cars(
        db: AsyncSession, 
        current_user: dict, 
        skip: int = 0, 
        limit: int = 100):
    '''
    Construct a query to get all customers_cars
    '''
    try:
        result = await db.execute(
            select(models.CustomerCar).offset(skip).limit(limit)
        )
        return result.scalars().all()
    except Exception as e:
        print(f"Database error in get_all_customers_cars: {e}")
        raise fetchErrorException
    
async def get_customer_car_by_id(
        customer_car_id: int,
        db: AsyncSession, 
        current_user: dict):
    '''
    Construct a query to get a customer_car by ID
    '''
    try:
        result = await db.execute(
            select(models.CustomerCar).filter(models.CustomerCar.customer_car_id == customer_car_id)
        )
        # Get customer_car data
        db_customer_car = result.scalar_one_or_none()
        # If customer_car not found, raise 404
        if db_customer_car is None:
            raise notFoundException
        return db_customer_car
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in get_customer_car_by_id: {e}")
        raise fetchErrorException
    
async def update_customer_car(
        customer_car_id: int,
        customer_car_update: schemas.CustomerCarUpdate,
        db: AsyncSession,
        current_user: dict):
    '''
    Construct a query to update a customer_car's information
    '''
    try:
        customer_car_data = await get_customer_car_by_id(customer_car_id, db, current_user)
            # Prepare update data
        update_data = customer_car_update.model_dump(exclude_unset=True)

        if "customer_id" in update_data:
            customer_res = await db.execute(select(models.Customer).where(models.Customer.customer_id == update_data["customer_id"]))
            if customer_res.scalar_one_or_none() is None:
                raise HTTPException(status_code=404, detail="Customer not found")

        if "car_id" in update_data:
            car_res = await db.execute(select(models.Car).where(models.Car.car_id == update_data["car_id"]))
            if car_res.scalar_one_or_none() is None:
                raise HTTPException(status_code=404, detail="Car not found")

        # Update other fields
        for field, value in update_data.items():
            setattr(customer_car_data, field, value)
        # Commit the transaction
        await db.commit()
        await db.refresh(customer_car_data)
        return customer_car_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in update_customer_car: {e}")
        raise fetchErrorException
    
async def delete_customer_car(
        customer_car_id: int,
        db: AsyncSession,
        current_user: dict):
    '''
    Construct a query to delete a customer_car
    '''
    try:
        customer_car_data = await get_customer_car_by_id(customer_car_id, db, current_user)

        await db.execute(
            delete(models.CustomerCar).where(models.CustomerCar.customer_car_id == customer_car_id)
        )
        await db.commit()
        return customer_car_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in delete_customer_car: {e}")
        raise fetchErrorException