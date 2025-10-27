from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from db import models, schemas, database
from db.database import get_db

router = APIRouter()

@router.post("/carros_clientes/", response_model=schemas.ClienteCarro)
async def create_cliente_carro(cliente_carro: schemas.ClienteCarroCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new cliente_carro
    """
    cliente_res = await db.execute(select(models.Cliente).where(models.Cliente.cliente_id == cliente_carro.cliente_id))
    if cliente_res.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Cliente not found")

    carro_res = await db.execute(select(models.Carro).where(models.Carro.carro_id == cliente_carro.carro_id))
    if carro_res.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Carro not found")

    db_cliente_carro = models.ClienteCarro(**cliente_carro.model_dump())
    db.add(db_cliente_carro)
    await db.commit()
    await db.refresh(db_cliente_carro)
    return db_cliente_carro

@router.get("/carros_clientes/", response_model=List[schemas.ClienteCarro])
async def read_clientes_carros(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all clientes_carros with pagination
    """
    result = await db.execute(
        select(models.ClienteCarro).offset(skip).limit(limit)
    )
    clientes_carros = result.scalars().all()
    return clientes_carros


@router.get("/carros_clientes/{cliente_carro_id}", response_model=schemas.ClienteCarro)
async def read_cliente_carro(cliente_carro_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific cliente_carro by ID
    """
    result = await db.execute(
        select(models.ClienteCarro).filter(models.ClienteCarro.cliente_carro_id == cliente_carro_id)
    )
    db_cliente_carro = result.scalar_one_or_none()
    if db_cliente_carro is None:
        raise HTTPException(status_code=404, detail="ClienteCarro not found")
    return db_cliente_carro

@router.put("/carros_clientes/{cliente_carro_id}", response_model=schemas.ClienteCarro)
async def update_cliente_carro(cliente_carro_id: int, cliente_carro: schemas.ClienteCarroUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update an existing cliente_carro (partial updates allowed)
    """
    result = await db.execute(
        select(models.ClienteCarro).where(models.ClienteCarro.cliente_carro_id == cliente_carro_id)
    )
    db_cliente_carro = result.scalar_one_or_none()
    if db_cliente_carro is None:
        raise HTTPException(status_code=404, detail="ClienteCarro not found")

    # Only update fields that are provided in the request
    cliente_data = cliente_carro.model_dump(exclude_unset=True)
    
    if "cliente_id" in cliente_data:
        cliente_res = await db.execute(select(models.Cliente).where(models.Cliente.cliente_id == cliente_data["cliente_id"]))
        if cliente_res.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Cliente not found")

    if "carro_id" in cliente_data:
        carro_res = await db.execute(select(models.Carro).where(models.Carro.carro_id == cliente_data["carro_id"]))
        if carro_res.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Carro not found")

    for key, value in cliente_data.items():
        setattr(db_cliente_carro, key, value)

    await db.commit()
    await db.refresh(db_cliente_carro)
    return db_cliente_carro

@router.delete("/carros_clientes/{cliente_carro_id}", response_model=schemas.ClienteCarro)
async def delete_cliente_carro(cliente_carro_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a cliente_carro
    """
    result = await db.execute(
        select(models.ClienteCarro).filter(models.ClienteCarro.cliente_carro_id == cliente_carro_id)
    )
    db_cliente_carro = result.scalar_one_or_none()
    if db_cliente_carro is None:
        raise HTTPException(status_code=404, detail="ClienteCarro not found")

    await db.execute(
        delete(models.ClienteCarro).where(models.ClienteCarro.cliente_carro_id == cliente_carro_id)
    )
    await db.commit()
    return db_cliente_carro
