from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from db import models, schemas, database
from db.database import get_db

router = APIRouter()

@router.post("/carros/", response_model=schemas.Carro)
async def create_carro(carro: schemas.CarroCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new carro
    """
    db_carro = models.Carro(**carro.model_dump())
    db.add(db_carro)
    await db.commit()
    await db.refresh(db_carro)
    return db_carro 

@router.get("/carros/", response_model=List[schemas.Carro])
async def read_carros(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all carros with pagination
    """
    result = await db.execute(
        select(models.Carro).offset(skip).limit(limit)
    )
    carros = result.scalars().all()
    return carros


@router.get("/carros/{carro_id}", response_model=schemas.Carro)
async def read_carro(carro_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific carro by ID
    """
    result = await db.execute(
        select(models.Carro).filter(models.Carro.carro_id == carro_id)
    )
    db_carro = result.scalar_one_or_none()
    if db_carro is None:
        raise HTTPException(status_code=404, detail="Carro not found")
    return db_carro

@router.put("/carros/{carro_id}", response_model=schemas.Carro)
async def update_carro(carro_id: int, carro: schemas.CarroUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update an existing carro (partial updates allowed)
    """
    result = await db.execute(
        select(models.Carro).where(models.Carro.carro_id == carro_id)
    )
    db_carro = result.scalar_one_or_none()
    if db_carro is None:
        raise HTTPException(status_code=404, detail="Carro not found")

    # Only update fields that are provided in the request
    carro_data = carro.model_dump(exclude_unset=True)
    for key, value in carro_data.items():
        setattr(db_carro, key, value)

    await db.commit()
    await db.refresh(db_carro)
    return db_carro

@router.delete("/carros/{carro_id}", response_model=schemas.Carro)
async def delete_carro(carro_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a carro
    """
    result = await db.execute(
        select(models.Carro).filter(models.Carro.carro_id == carro_id)
    )
    db_carro = result.scalar_one_or_none()
    if db_carro is None:
        raise HTTPException(status_code=404, detail="Carro not found")

    await db.execute(
        delete(models.Carro).where(models.Carro.carro_id == carro_id)
    )
    await db.commit()
    return db_carro
