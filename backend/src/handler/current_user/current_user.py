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


# ---------------- Current user's workshop parts endpoint ----------------
@router.post("/workshops/parts", response_model=schemas.PartWorkshop, summary="Create part for current user's workshop")
@limiter.limit("10/minute")
async def create_current_user_workshop_part(
    request: Request,
    user: user_dependency,
    part: schemas.PartWorkshopCreate,
    db: AsyncSession = Depends(get_db)
    
):
    """
    Create a part associated with the currently authenticated user's workshop
    """
    return await service.create_current_user_workshop_part(user, part, db)

@router.get("/workshops/parts", response_model=List[schemas.PartWorkshop], summary="Get parts of current user's workshop")
@limiter.limit("10/minute")
async def read_current_user_workshop_parts(
    request: Request,
    user: user_dependency,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the parts associated with the currently authenticated user's workshop
    """
    return await service.get_current_user_workshop_parts(user, db)

@router.patch("/workshops/parts/{part_id}", response_model=schemas.PartWorkshop, summary="Update part of current user's workshop")
@limiter.limit("10/minute")
async def update_current_user_workshop_part(
    request: Request,
    user: user_dependency,
    part_id: int,
    part_update: schemas.PartWorkshopUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a part associated with the currently authenticated user's workshop
    """
    return await service.update_current_user_workshop_part(user, part_id, part_update, db)

@router.delete("/workshops/parts/{part_id}", response_model=schemas.PartWorkshop, summary="Delete part of current user's workshop")
@limiter.limit("10/minute")
async def delete_current_user_workshop_part(
    request: Request,
    user: user_dependency,
    part_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a part associated with the currently authenticated user's workshop
    """
    return await service.delete_current_user_workshop_part(user, part_id, db)




# ---------------- Current user's workshop customers endpoint ----------------

@router.get("/workshops/customers/", response_model=List[schemas.Customer], summary="Get customers of current user's workshop")
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

@router.post("/workshops/customers/", response_model=schemas.Customer, summary="Create customer for current user's workshop")
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

@router.patch("/workshops/customers/{customer_id}", response_model=schemas.Customer, summary="Update customer of current user's workshop")
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


@router.delete("/workshops/customers/{customer_id}", response_model=schemas.Customer, summary="Delete customer of current user's workshop")
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

