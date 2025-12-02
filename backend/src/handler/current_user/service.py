from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from auth.auth import get_current_user, pwd_context, admin_required, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from db import models, schemas
from exceptions.exceptions import notFoundException, fetchErrorException
from db.database import get_db

# ---------------- Current user endpoints ----------------
async def get_current_user_info(
    current_user: dict, 
    db: AsyncSession):
    """
    Get current logged-in user information
    """
    try:
        result = await db.execute(
            select(models.User).where(models.User.user_id == current_user["user_id"])
        )
        user = result.scalars().first()
        if not user:
            raise notFoundException("User not found")
        return user
    except Exception as e:
        raise fetchErrorException(f"Error fetching user info: {str(e)}")
    
async def patch_current_user_info(
    user_update: schemas.CurrentUserUpdate,
    current_user: dict,
    db: AsyncSession):
    """
    Update current logged-in user information
    """
    try:
        result = await db.execute(
            select(models.User).where(models.User.user_id == current_user["user_id"])
        )
        db_user = result.scalars().first()
        if not db_user:
            raise notFoundException  # Don't pass message if it's HTTPException
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        await db.commit()
        await db.refresh(db_user)
        return db_user  # Return just db_user, not tuple
    except HTTPException:
        raise  # Let HTTPExceptions propagate
    except Exception as e:
        print(f"Database error in patch_current_user_info: {e}")
        raise fetchErrorException
    
async def update_current_user_password(
    password_update: schemas.CurrentUserPassword,
    current_user: dict,
    db: AsyncSession):
    """
    Update current logged-in user's password
    """
    try:
        result = await db.execute(
            select(models.User).where(models.User.user_id == current_user["user_id"])
        )
        db_user = result.scalars().first()
        if not db_user:
            raise notFoundException  # Don't pass message if it's HTTPException
        if not pwd_context.verify(password_update.old_password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Old password is incorrect")
        
        hashed_password = pwd_context.hash(password_update.new_password)
        db_user.hashed_password = hashed_password

        # Increment token version to invalidate all existing tokens
        db_user.token_version += 1

        await db.commit()
        await db.refresh(db_user)

        new_token = create_access_token(
        db_user.email, 
        db_user.user_id,
        db_user.token_version,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
        return {
            "message": "Password updated successfully",
            "access_token": new_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise  # Let HTTPExceptions propagate
    except Exception as e:
        print(f"Database error in update_current_user_password: {e}")
        raise fetchErrorException

async def delete_current_user_account(
    current_user: dict,
    db: AsyncSession):
    """
    Delete current logged-in user's account
    """
    try:
        result = await db.execute(
            select(models.User).where(models.User.user_id == current_user["user_id"])
        )
        db_user = result.scalars().first()
        if not db_user:
            raise notFoundException("User not found")

        await db.delete(db_user)
        await db.commit()
        return db_user
    except HTTPException:
        raise  # Let HTTPExceptions propagate
    except Exception as e:
        print(f"Database error in delete_current_user_account: {e}")
        raise fetchErrorException
# ---------------- End of current user's info endpoints ----------------


