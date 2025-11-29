from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from db import models, schemas
from exceptions.exceptions import notFoundException, fetchErrorException

# ---------------- All workshops functions (ADMIN REQUIRED)----------------
async def create_workshop(
        workshop: schemas.WorkshopCreate,
        db: AsyncSession,
        current_user: dict):
    '''
    Construct a query to create a new workshop
    '''
    try:
        db_workshop = models.Workshop(**workshop.model_dump())

        db.add(db_workshop)
        await db.commit()
        await db.refresh(db_workshop)
        return db_workshop
    except Exception as e:
        print(f"Database error in create_workshop: {e}")
        raise fetchErrorException
    
async def get_all_workshops(
        db: AsyncSession, 
        current_user: dict, 
        skip: int = 0, 
        limit: int = 100):
    '''
    Construct a query to get all workshops
    '''
    try:
        result = await db.execute(
            select(models.Workshop).offset(skip).limit(limit)
        )
        return result.scalars().all()
    except Exception as e:
        print(f"Database error in get_all_workshops: {e}")
        raise fetchErrorException
    
async def get_workshop_by_id(
        workshop_id: int,
        db: AsyncSession, 
        current_user: dict):
    '''
    Construct a query to get a workshop by ID
    '''
    try:
        result = await db.execute(
            select(models.Workshop).filter(models.Workshop.workshop_id == workshop_id)
        )
        # Get workshop data
        db_workshop = result.scalar_one_or_none()
        # If workshop not found, raise 404
        if db_workshop is None:
            raise notFoundException
        return db_workshop
    except Exception as e:
        print(f"Database error in get_workshop_by_id: {e}")
        raise fetchErrorException
    
async def update_workshop(
        workshop_id: int,
        workshop_update: schemas.WorkshopUpdate,
        db: AsyncSession,
        current_user: dict):
    '''
    Construct a query to update a workshop's information
    '''
    try:
        workshop_data = await get_workshop_by_id(workshop_id, db, current_user)
            # Prepare update data
        update_data = workshop_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(workshop_data, field, value)

        await db.commit()
        await db.refresh(workshop_data)
        return workshop_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in update_workshop: {e}")
        raise fetchErrorException
    
async def delete_workshop(
        workshop_id: int,
        db: AsyncSession,
        current_user: dict):
    '''
    Construct a query to delete a workshop
    '''
    try:
        workshop_data = await get_workshop_by_id(workshop_id, db, current_user)

        await db.execute(
            delete(models.Workshop).where(models.Workshop.workshop_id == workshop_id)
        )
        await db.commit()
        return workshop_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in delete_workshop: {e}")
        raise fetchErrorException
    
# ---------------- End of all workshops functions FOR ADMINS ----------------

# ---------------- Current user's workshop functions ----------------
def get_current_user_workshop_id(user: dict) -> int:
    """
    Utility function to get the workshop ID of the current user
    """
    return user.get("workshop_id")

async def create_current_user_workshop(
    current_user: dict,
    workshop: schemas.WorkshopCreate,
    db: AsyncSession
):
    """
    Create a workshop for the current logged-in user
    """
    if get_current_user_workshop_id(current_user) != 1:
        raise HTTPException(status_code=400, detail="User already has a workshop")
    
    create_workshop_model = models.Workshop(
        workshop_name=workshop.workshop_name,
        address=workshop.address,
        opening_hours=workshop.opening_hours,
        closing_hours=workshop.closing_hours
    )
    db.add(create_workshop_model)
    await db.commit()
    await db.refresh(create_workshop_model)

    # Update user's workshop_id
    result = await db.execute(
        select(models.User).filter(models.User.user_id == current_user["user_id"])
    )
    db_user = result.scalar_one_or_none()
    db_user.workshop_id = create_workshop_model.workshop_id
    await db.commit()
    await db.refresh(db_user)
    return create_workshop_model

async def get_current_user_workshop(
    current_user: dict,
    db: AsyncSession
):
    """
    Get the workshop associated with the current logged-in user
    """
    result = await db.execute(
        select(models.Workshop).filter(models.Workshop.workshop_id == current_user["workshop_id"])
    )
    workshop = result.scalars().first()
    if not workshop:
        raise notFoundException("Workshop not found")
    return [workshop]

async def patch_current_user_workshop(
    current_user: dict,
    workshop_update: schemas.WorkshopUpdate,
    db: AsyncSession
):
    """
    Update the workshop associated with the current logged-in user
    """
    if get_current_user_workshop_id(current_user) == 1:
        raise HTTPException(status_code=400, detail="User has no workshop to update")
    
    result = await db.execute(
        select(models.Workshop).filter(models.Workshop.workshop_id == current_user["workshop_id"])
    )
    db_workshop = result.scalars().first()
    if not db_workshop:
        raise notFoundException(status_code=404, detail="Workshop not found")
    
    update_data = workshop_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_workshop, field, value)

    await db.commit()
    await db.refresh(db_workshop)
    return db_workshop