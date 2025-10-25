from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from db import models, schemas, database
from db.database import get_db

router = APIRouter()

@router.post("/clientes/", response_model=schemas.Cliente)
async def create_cliente(cliente: schemas.ClienteCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new cliente
    """
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    return db_cliente

@router.get("/clientes/", response_model=List[schemas.Cliente])
async def read_clientes(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all clientes with pagination
    """
    result = await db.execute(
        select(models.Cliente).offset(skip).limit(limit)
    )
    clientes = result.scalars().all()
    return clientes


@router.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
async def read_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific cliente by ID
    """
    result = await db.execute(
        select(models.Cliente).filter(models.Cliente.cliente_id == cliente_id)
    )
    db_cliente = result.scalar_one_or_none()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente

@router.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
async def update_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update an existing cliente (partial updates allowed)
    """
    result = await db.execute(
        select(models.Cliente).where(models.Cliente.cliente_id == cliente_id)
    )
    db_cliente = result.scalar_one_or_none()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")

    # Only update fields that are provided in the request
    cliente_data = cliente.model_dump(exclude_unset=True)
    for key, value in cliente_data.items():
        setattr(db_cliente, key, value)

    await db.commit()
    await db.refresh(db_cliente)
    return db_cliente

@router.delete("/clientes/{cliente_id}", response_model=schemas.Cliente)
async def delete_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a cliente
    """
    result = await db.execute(
        select(models.Cliente).filter(models.Cliente.cliente_id == cliente_id)
    )
    db_cliente = result.scalar_one_or_none()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")

    await db.execute(
        delete(models.Cliente).where(models.Cliente.cliente_id == cliente_id)
    )
    await db.commit()
    return db_cliente
