from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from auth.auth import get_current_user, pwd_context
from db import models, schemas
from exceptions.exceptions import notFoundException, fetchErrorException


router = APIRouter()


# ---------------- All user functions ----------------

def current_user_role(user: dict = Depends(get_current_user)):
    '''
    Get the role of the current user from the token payload
    '''
    return user["role"]

async def get_all_users_query(db: AsyncSession, current_user: dict, skip: int = 0, limit: int = 100):
    '''
    Construct a query to get all users with pagination
    '''
    try:
        result = await db.execute(
            select(models.User).offset(skip).limit(limit)
        )
        users = result.scalars().all()
        return users
    except:
        raise fetchErrorException
    

async def get_user_by_id_query(db: AsyncSession, current_user: dict, user_id: int):
    '''
    Construct a query to get a user by ID
    '''
    try:
        result = await db.execute(
            select(models.User).filter(models.User.user_id == user_id)
        )
        # Get user data
        db_user = result.scalar_one_or_none()
        # If user not found, raise 404
        if db_user is None:
            raise notFoundException
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in get_user_by_id_query: {e}")
        raise fetchErrorException

async def update_user_query(db: AsyncSession, current_user: dict, user_data: dict, user_update: schemas.UserUpdate):
    '''
    Construct a query to update a user's information
    '''
    try:
        user_data = user_data
            # Prepare update data
        update_data = user_update.model_dump(exclude_unset=True)
        # handle password hashing specially
        if "password" in update_data:
            plain = update_data.pop("password")
            if plain:
                user_data.hashed_password = pwd_context.hash(plain)
        # Update other fields
        for field, value in update_data.items():
            setattr(user_data, field, value)
        # Commit the transaction
        await db.commit()
        await db.refresh(user_data)
        return user_data
    except:
        raise fetchErrorException