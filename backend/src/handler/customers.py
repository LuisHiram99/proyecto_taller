from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Annotated, List
from auth.auth import get_current_user, is_admin


from db import models, schemas, database
from db.database import get_db

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


# ---------------- All customers endpoints ----------------


@router.post("/customers/", response_model=schemas.Customer)
async def create_customer(current_user: user_dependency, customer: schemas.CustomerCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new customer
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    data = customer.model_dump()
    db_customer = models.Customer(**data)

    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

@router.get("/customers/", response_model=List[schemas.Customer])
async def read_customers(current_user: user_dependency, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all customers with pagination
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")

    result = await db.execute(
        select(models.Customer).offset(skip).limit(limit)
    )
    customers = result.scalars().all()
    return customers

@router.get("/customers/{customer_id}", response_model=schemas.Customer)
async def read_customer(current_user: user_dependency, customer_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific customer by ID
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    result = await db.execute(
        select(models.Customer).filter(models.Customer.customer_id == customer_id)
    )
    db_customer = result.scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/customers/{customer_id}", response_model=schemas.Customer)
async def update_customer(current_user: user_dependency, customer_id: int, customer: schemas.CustomerUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a customer's information
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
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
async def delete_customer(current_user: user_dependency, customer_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a customer
    """
    # if the current user is not admin, raise 403
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Operation not permitted")

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


