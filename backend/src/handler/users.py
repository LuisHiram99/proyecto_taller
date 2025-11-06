from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Annotated, List
from auth.auth import get_current_user, pwd_context
from repositories.user_repository import *
from exceptions.exceptions import notAdminException, notFoundException

from db import models, schemas, database
from db.database import get_db

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


# ---------------- All user endpoints ----------------

@router.get("/users/", response_model=List[schemas.User], summary="Get all users")
async def read_users(user: user_dependency, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all users with pagination
    """
    # if the current user is not admin, raise 403
    if current_user_role(user) != "admin":
        raise notAdminException
    # Get all users from the database
    users = await get_all_users_query(db, user, skip, limit)
    return users

@router.get("/users/{user_id}", response_model=schemas.User, summary="Get user by ID")
async def read_user(user: user_dependency, user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific user by ID
    """
    # if the current user is not admin, raise 403
    if current_user_role(user) != "admin":
        raise notAdminException
    # Get the user from the database
    user_data = await get_user_by_id_query(db, user, user_id)
    return user_data

@router.put("/users/{user_id}", response_model=schemas.User, summary="Update user by ID")
async def update_user(
    current_user: user_dependency,
    user_id: int,
    user: schemas.UserUpdate,           
    db: AsyncSession = Depends(get_db),
):
    """
    Update a user's information
    """
    # if the current user is not admin, raise 403
    if current_user_role(current_user) != "admin":
        raise notAdminException

    # Get the user to be updated
    user_data = await get_user_by_id_query(db, current_user, user_id)
    # If user not found, raise 404
    if user_data is None:
        raise notFoundException
    # Prepare update data
    updated_user = await update_user_query(db, current_user, user_data, user)
    return updated_user

@router.delete("/users/{user_id}", response_model=schemas.User, summary="Delete user by ID")
async def delete_user(user: user_dependency, user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a user
    """
    # First we check if the current user has admin role, otherwise raise 403
    if current_user_role(user) != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    # Get the user to be deleted
    result = await db.execute(
        select(models.User).filter(models.User.user_id == user_id)
    )
    db_user = result.scalar_one_or_none()
    # If user not found, raise 404
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    await db.execute(
        delete(models.User).where(models.User.user_id == user_id)
    )

    # Commit the transaction
    await db.commit()
    return db_user
