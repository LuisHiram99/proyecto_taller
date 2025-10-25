from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from db import models, schemas, database
from db.database import get_db

router = APIRouter()

@router.post("/usuarios/", response_model=schemas.Usuario)
async def create_usuario(usuario: schemas.UsuarioCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new usuario
    """
    db_usuario = models.Usuario(**usuario.model_dump())
    db.add(db_usuario)
    await db.commit()
    await db.refresh(db_usuario)
    return db_usuario

@router.get("/usuarios/", response_model=List[schemas.Usuario])
async def read_usuarios(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all usuarios with pagination
    """
    result = await db.execute(
        select(models.Usuario).offset(skip).limit(limit)
    )
    usuarios = result.scalars().all()
    return usuarios

@router.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
async def read_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific usuario by ID
    """
    result = await db.execute(
        select(models.Usuario).filter(models.Usuario.usuario_id == usuario_id)
    )
    db_usuario = result.scalar_one_or_none()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

@router.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
async def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: AsyncSession = Depends(get_db)):
    """
    Update a usuario's information
    """
    result = await db.execute(
        select(models.Usuario).filter(models.Usuario.usuario_id == usuario_id)
    )
    db_usuario = result.scalar_one_or_none()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
        
    for field, value in usuario.model_dump().items():
        setattr(db_usuario, field, value)
        
    await db.commit()
    await db.refresh(db_usuario)
    return db_usuario

@router.delete("/usuarios/{usuario_id}", response_model=schemas.Usuario)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a usuario
    """
    result = await db.execute(
        select(models.Usuario).filter(models.Usuario.usuario_id == usuario_id)
    )
    db_usuario = result.scalar_one_or_none()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
        
    await db.execute(
        delete(models.Usuario).where(models.Usuario.usuario_id == usuario_id)
    )
    await db.commit()
    return db_usuario
