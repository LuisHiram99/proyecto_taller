from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from auth.auth import get_current_user, pwd_context, admin_required
from db import models, schemas
from exceptions.exceptions import notFoundException, fetchErrorException

# ---------------- All customers functions ----------------
async def create_customer(
        customer: schemas.CustomerCreate,
        db: AsyncSession,
        current_user: dict):
    '''
    Construct a query to create a new customer
    '''
    try:
        db_customer = models.Customer(**customer.model_dump())

        db.add(db_customer)
        await db.commit()
        await db.refresh(db_customer)
        return db_customer
    except Exception as e:
        print(f"Database error in create_customer: {e}")
        raise fetchErrorException

async def get_all_customers(
        db: AsyncSession, 
        current_user: dict, 
        skip: int = 0, 
        limit: int = 100):
    '''
    Construct a query to get all customers
    '''
    try:
        result = await db.execute(
            select(models.Customer).offset(skip).limit(limit)
        )
        return result.scalars().all()
    except Exception as e:
        print(f"Database error in get_all_customers: {e}")
        raise fetchErrorException
    
async def get_customer_by_id(
        customer_id: int,
        db: AsyncSession, 
        current_user: dict):
    '''
    Construct a query to get a customer by ID
    '''
    try:
        result = await db.execute(
            select(models.Customer).filter(models.Customer.customer_id == customer_id)
        )
        # Get customer data
        db_customer = result.scalar_one_or_none()
        # If customer not found, raise 404
        if db_customer is None:
            raise notFoundException
        return db_customer
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in get_customer_by_id: {e}")
        raise fetchErrorException
    
async def update_customer(
        customer_id: int, 
        customer_update: schemas.CustomerUpdate,
        db: AsyncSession,
        current_user: dict):
    '''
    Construct a query to update a customer's information
    '''
    try:
        customer_data = await get_customer_by_id(customer_id, db, current_user)
            # Prepare update data
        update_data = customer_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(customer_data, key, value)
        await db.commit()
        await db.refresh(customer_data)
        return customer_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in update_customer: {e}")
        raise fetchErrorException
    
async def delete_customer(
        customer_id: int,
        db: AsyncSession,
        current_user: dict):
    '''
    Construct a query to delete a customer
    '''
    try:
        result = await db.execute(
            select(models.Customer).filter(models.Customer.customer_id == customer_id)
        )
        db_customer = result.scalar_one_or_none()
        # If customer not found, raise 404
        if db_customer is None:
            raise notFoundException

        await db.execute(
            delete(models.Customer).where(models.Customer.customer_id == customer_id)
        )
        await db.commit()
        return db_customer
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in delete_customer: {e}")
        raise fetchErrorException
    
