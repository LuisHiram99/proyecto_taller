from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Annotated
from auth.auth import get_current_user



from db import models, schemas
from db.database import get_db

router = APIRouter(prefix="/me", tags=["current_user"])

user_dependency = Annotated[dict, Depends(get_current_user)]

# ---------------- Current user's info endpoints ----------------

@router.get("/", response_model=schemas.User)
async def read_current_user(user: user_dependency, db: AsyncSession = Depends(get_db)):
    """
    Get the currently authenticated user
    """
    result = await db.execute(
        select(models.User).filter(models.User.user_id == user["user_id"])
    )
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/", response_model=schemas.User)
async def update_current_user(
    current_user: user_dependency,
    user: schemas.UserUpdate,           
    db: AsyncSession = Depends(get_db),
):
    """
    Update the currently authenticated user's information
    """
    result = await db.execute(
        select(models.User).filter(models.User.user_id == current_user["user_id"])
    )
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.model_dump(exclude_unset=True)
    # handle password hashing specially
    if "password" in update_data:
        plain = update_data.pop("password")
        if plain:
            db_user.hashed_password = pwd_context.hash(plain)
    # Update other fields
    for field, value in update_data.items():
        setattr(db_user, field, value)
    # Commit the transaction
    await db.commit()
    await db.refresh(db_user)
    return db_user, update_data

@router.delete("/", response_model=schemas.User)
async def delete_current_user(user: user_dependency, db: AsyncSession = Depends(get_db)):
    """
    Delete the currently authenticated user
    """
    result = await db.execute(
        select(models.User).filter(models.User.user_id == user["user_id"])
    )
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.execute(
        delete(models.User).where(models.User.user_id == user["user_id"])
    )
    await db.commit()
    return db_user

# ---------------- End of current user's info endpoints ----------------


# ---------------- Current user's workshop related functions ----------------
@router.get("/workshop/", response_model=List[schemas.Workshop], summary="Get current user's workshop")
async def read_current_user_workshops(
    user: user_dependency,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the workshop associated with the currently authenticated user
    """
    result = await db.execute(
        select(models.Workshop).filter(models.Workshop.workshop_id == user["workshop_id"])
    )
    workshops = result.scalars().all()
    return workshops


@router.get("/workshop/customers/", response_model=List[schemas.Customer], summary="Get customers of current user's workshop")
async def read_current_user_workshop_customers(
    user: user_dependency,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the customers associated with the currently authenticated user's workshop
    """
    workshop_id = get_current_user_workshop_id(user)
    result = await db.execute(
        select(models.Customer).filter(models.Customer.workshop_id == workshop_id)
    )
    customers = result.scalars().all()
    return customers

def get_current_user_workshop_id(user: dict) -> int:
    """
    Utility function to get the workshop ID of the current user
    """
    return user.get("workshop_id")