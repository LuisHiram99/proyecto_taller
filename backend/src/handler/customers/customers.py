from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Annotated, List
from auth.auth import admin_required, get_current_user, is_admin
from . import service
from ..rate_limiter import limiter

from db import models, schemas, database
from db.database import get_db

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


# ---------------- All customers endpoints ----------------


@router.post("/customers/", response_model=schemas.Customer)
@limiter.limit("10/minute")
async def create_customer(
    request: Request,
    customer: schemas.CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(admin_required)):
    """
    Create a new customer
    """

    return await service.create_customer(customer, db, current_user)

@router.get("/customers/", response_model=List[schemas.Customer])
@limiter.limit("10/minute")
async def read_customers(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(admin_required)):
    """
    Get all customers with pagination
    """
    return await service.get_all_customers(db, current_user, skip, limit)

@router.get("/customers/{customer_id}", response_model=schemas.Customer)
@limiter.limit("10/minute")
async def read_customer(
    request: Request,
    customer_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(admin_required)):
    """
    Get a specific customer by ID
    """
    return await service.get_customer_by_id(customer_id, db, current_user)

@router.put("/customers/{customer_id}", response_model=schemas.Customer)
@limiter.limit("10/minute")
async def update_customer(
    request: Request,
    current_user: user_dependency, 
    customer_id: int, 
    customer_update: schemas.CustomerUpdate, 
    db: AsyncSession = Depends(get_db)):
    """
    Update a customer's information
    """
    return await service.update_customer(customer_id, customer_update, db, current_user)

@router.delete("/customers/{customer_id}", response_model=schemas.Customer)
async def delete_customer(
    request: Request, 
    current_user: user_dependency, 
    customer_id: int, 
    db: AsyncSession = Depends(get_db)):
    """
    Delete a customer
    """
    return await service.delete_customer(customer_id, db, current_user)


