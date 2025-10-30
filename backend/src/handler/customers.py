from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List


from db import models, schemas, database
from db.database import get_db

router = APIRouter()


@router.post("/customers/", response_model=schemas.Customer)
async def create_customer(customer: schemas.CustomerCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new customer
    """
    data = customer.model_dump()
    db_customer = models.Customer(**data)

    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

@router.get("/customers/", response_model=List[schemas.Customer])
async def read_customers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all customers with pagination
    """
    result = await db.execute(
        select(models.Customer).offset(skip).limit(limit)
    )
    customers = result.scalars().all()
    return customers

@router.get("/customers/{customer_id}", response_model=schemas.Customer)
async def read_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific customer by ID
    """
    result = await db.execute(
        select(models.Customer).filter(models.Customer.customer_id == customer_id)
    )
    db_customer = result.scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/customers/{customer_id}", response_model=schemas.Customer)
async def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a customer's information
    """
    result = await db.execute(
        select(models.Customer).filter(models.Customer.customer_id == customer_id)
    )
    db_customer = result.scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_customer, field, value)

    await db.commit()
    await db.refresh(db_customer)
    return db_customer

@router.delete("/customers/{customer_id}", response_model=schemas.Customer)
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a customer
    """
    result = await db.execute(
        select(models.Customer).filter(models.Customer.customer_id == customer_id)
    )
    db_customer = result.scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    await db.execute(
        delete(models.Customer).where(models.Customer.customer_id == customer_id)
    )
    await db.commit()
    return db_customer
