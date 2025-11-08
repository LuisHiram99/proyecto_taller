from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Annotated
from auth.auth import get_current_user, is_admin, admin_required
from . import service
from ..rate_limiter import limiter


from db import models, schemas
from db.database import get_db

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


# ---------------- All workshop endpoints ----------------
@router.post("/workshops/", response_model=schemas.Workshop)
@limiter.limit("10/minute")
async def create_workshop( 
    request: Request,
    workshop: schemas.WorkshopCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(admin_required)):
    """
    Create a new workshop
    """
    return await service.create_workshop(workshop, db, current_user)

@router.get("/workshops/", response_model=List[schemas.Workshop])
@limiter.limit("10/minute")
async def read_workshops(
    request: Request,
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(admin_required), 
    skip: int = 0, 
    limit: int = 100):
    """
    Get all workshops with pagination
    """
    return await service.get_all_workshops(db, current_user, skip, limit)

@router.get("/workshops/{workshop_id}", response_model=schemas.Workshop)
@limiter.limit("10/minute")
async def read_workshop(
    request: Request,
    workshop_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(admin_required)):
    """
    Get a specific workshop by ID
    """
    return await service.get_workshop_by_id(workshop_id, db, current_user)

@router.put("/workshops/{workshop_id}", response_model=schemas.Workshop)
@limiter.limit("10/minute")
async def update_workshop(
    request: Request,
    workshop_id: int, 
    workshop_update: schemas.WorkshopUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(admin_required)
):
    """
    Update a workshop's information
    """
    return await service.update_workshop(workshop_id, workshop_update, db, current_user)

@router.delete("/workshops/{workshop_id}", response_model=schemas.Workshop)
@limiter.limit("10/minute")
async def delete_workshop(
    request: Request,
    workshop_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(admin_required)):
    """
    Delete a workshop
    """
    return await service.delete_workshop(workshop_id, db, current_user)
