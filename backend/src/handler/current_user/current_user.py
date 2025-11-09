from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Annotated
from auth.auth import get_current_user, admin_required, pwd_context
from auth.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from . import service
from ..rate_limiter import limiter



from db import models, schemas
from db.database import get_db

router = APIRouter(prefix="/me", tags=["current_user"])

user_dependency = Annotated[dict, Depends(get_current_user)]

# ---------------- Current user's info endpoints ----------------

@router.get("/", response_model=schemas.User)
@limiter.limit("10/minute")
async def read_current_user(request: Request, user: user_dependency, db: AsyncSession = Depends(get_db)):
    """
    Get the currently authenticated user
    """
    return await service.get_current_user_info(user, db)


@router.patch("/", response_model=schemas.CurrentUserUpdate)
@limiter.limit("10/minute")
async def patch_current_user(
    request: Request,
    current_user: user_dependency,
    user: schemas.CurrentUserUpdate,           
    db: AsyncSession = Depends(get_db),
):
    """
    Partially update the currently authenticated user's information
    """
    return await service.patch_current_user_info(user, current_user, db)

@router.put("/password")
@limiter.limit("10/minute")
async def update_current_user_password(
    request: Request,
    current_user: user_dependency,
    password_update: schemas.CurrentUserPassword,
    db: AsyncSession = Depends(get_db),
):
    """
    Update the currently authenticated user's password and return a new token.
    This invalidates all existing tokens by incrementing the token version.
    """
    return await service.update_current_user_password(password_update, current_user, db)

@router.delete("/", response_model=schemas.User)
@limiter.limit("10/minute")
async def delete_current_user(request: Request, user: user_dependency, db: AsyncSession = Depends(get_db)):
    """
    Delete the currently authenticated user
    """
    return await service.delete_current_user_account(user, db)

# ---------------- End of current user's info endpoints ----------------


# ---------------- Current user's workshop related functions ----------------
@router.post("/workshop/", response_model=schemas.Workshop, summary="Create workshop for current user")
@limiter.limit("10/minute")
async def create_current_user_workshop(
    request: Request,
    user: user_dependency,
    workshop: schemas.WorkshopCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a workshop associated with the currently authenticated user
    """

    return await service.create_current_user_workshop(user, workshop, db)

@router.get("/workshop/", response_model=schemas.Workshop, summary="Get current user's workshop")
@limiter.limit("10/minute") 
async def read_current_user_workshop(
    request: Request,
    user: user_dependency,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the workshop associated with the currently authenticated user
    """
    return await service.get_current_user_workshop(user, db)

@router.patch("/workshop/", response_model=schemas.Workshop, summary="Update current user's workshop")
@limiter.limit("10/minute")
async def update_current_user_workshop(
    request: Request,
    user: user_dependency,
    workshop: schemas.WorkshopUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update the workshop associated with the currently authenticated user
    """
    return await service.patch_current_user_workshop(user, workshop, db)

# ---------------- End of current user's workshop related functions ----------------


# ---------------- Current user's workshop customers endpoint ----------------

@router.get("/workshop/customers/", response_model=List[schemas.Customer], summary="Get customers of current user's workshop")
@limiter.limit("10/minute")
async def read_current_user_workshop_customers(
    request: Request,
    user: user_dependency,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the customers associated with the currently authenticated user's workshop
    """
    return await service.get_current_user_workshop_customers(user, db)

@router.post("/workshop/customers/", response_model=schemas.Customer, summary="Create customer for current user's workshop")
@limiter.limit("10/minute")
async def create_current_user_workshop_customer(
    request: Request,
    user: user_dependency,
    customer: schemas.CustomerCreateForWorkshop,  # Changed this
    db: AsyncSession = Depends(get_db)
):
    """
    Create a customer associated with the currently authenticated user's workshop
    """
    return await service.create_current_user_workshop_customer(user, customer, db)

@router.patch("/workshop/customers/{customer_id}", response_model=schemas.Customer, summary="Update customer of current user's workshop")
@limiter.limit("10/minute")
async def patch_current_user_workshop_customer(
    request: Request,
    user: user_dependency,
    customer_id: int,
    customer: schemas.CustomerUpdateForWorkshop,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a customer associated with the currently authenticated user's workshop
    """
    return await service.patch_current_user_workshop_customer(user, customer_id, customer, db)


@router.delete("/workshop/customers/{customer_id}", response_model=schemas.Customer, summary="Delete customer of current user's workshop")
@limiter.limit("10/minute")
async def delete_current_user_workshop_customer(
    request: Request,
    user: user_dependency,
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a customer associated with the currently authenticated user's workshop
    """
    return await service.delete_current_user_workshop_customer(user, customer_id, db)

