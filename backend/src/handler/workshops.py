from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Annotated
from auth.auth import get_current_user



from db import models, schemas
from db.database import get_db

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


# ---------------- All workshop endpoints ----------------
@router.post("/workshops/", response_model=schemas.Workshop)
async def create_workshop(workshop: schemas.WorkshopCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new workshop
    """
    data = workshop.model_dump()
    db_workshop = models.Workshop(**data)

    db.add(db_workshop)
    await db.commit()
    await db.refresh(db_workshop)
    return db_workshop

@router.get("/workshops/", response_model=List[schemas.Workshop])
async def read_workshops(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all workshops with pagination
    """
    result = await db.execute(
        select(models.Workshop).offset(skip).limit(limit)
    )
    workshops = result.scalars().all()
    return workshops

@router.get("/workshops/{workshop_id}", response_model=schemas.Workshop)
async def read_workshop(workshop_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific workshop by ID
    """
    result = await db.execute(
        select(models.Workshop).filter(models.Workshop.workshop_id == workshop_id)
    )
    db_workshop = result.scalar_one_or_none()
    if db_workshop is None:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return db_workshop

@router.put("/workshops/{workshop_id}", response_model=schemas.Workshop)
async def update_workshop(workshop_id: int, workshop: schemas.WorkshopUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a workshop's information
    """
    result = await db.execute(
        select(models.Workshop).filter(models.Workshop.workshop_id == workshop_id)
    )
    db_workshop = result.scalar_one_or_none()
    if db_workshop is None:
        raise HTTPException(status_code=404, detail="Workshop not found")

    update_data = workshop.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_workshop, field, value)

    await db.commit()
    await db.refresh(db_workshop)
    return db_workshop

@router.delete("/workshops/{workshop_id}", response_model=schemas.Workshop)
async def delete_workshop(workshop_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a workshop
    """
    result = await db.execute(
        select(models.Workshop).filter(models.Workshop.workshop_id == workshop_id)
    )
    db_workshop = result.scalar_one_or_none()
    if db_workshop is None:
        raise HTTPException(status_code=404, detail="Workshop not found")

    await db.execute(
        delete(models.Workshop).where(models.Workshop.workshop_id == workshop_id)
    )
    await db.commit()
    return db_workshop
