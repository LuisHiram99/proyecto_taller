from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from passlib.context import CryptContext


from db import models, schemas, database
from db.database import get_db

router = APIRouter()

# password hashing context with Argon2
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=2,      # number of iterations
    argon2__memory_cost=102400,  # memory usage in kibibytes (100 MB)
    argon2__parallelism=8     # number of parallel threads
)

@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user
    """
    data = user.model_dump()
    # remove password before creating the SQLAlchemy model (we store hashed password)
    plain_password = data.pop("password", None)
    if not plain_password:
        raise HTTPException(status_code=400, detail="Password is required")
        
    db_user = models.User(**data)
    db_user.hashed_password = pwd_context.hash(plain_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all users with pagination
    """
    result = await db.execute(
        select(models.User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific user by ID
    """
    result = await db.execute(
        select(models.User).filter(models.User.user_id == user_id)
    )
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a user's information
    """
    result = await db.execute(
        select(models.User).filter(models.User.user_id == user_id)
    )
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.model_dump(exclude_unset=True)
    # handle password specially
    if "password" in update_data:
        plain = update_data.pop("password")
        if plain:
            db_user.hashed_password = pwd_context.hash(plain)

    for field, value in update_data.items():
        setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a user
    """
    result = await db.execute(
        select(models.User).filter(models.User.user_id == user_id)
    )
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.execute(
        delete(models.User).where(models.User.user_id == user_id)
    )
    await db.commit()
    return db_user
