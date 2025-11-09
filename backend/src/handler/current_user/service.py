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


# ---------------- Current user's workshop related functions ----------------

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
    return workshop

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

# ---------------- End of current user's workshop related functions ----------------

# ---------------- Current user's workshop customers endpoint ----------------
async def get_current_user_workshop_customers(
    current_user: dict,
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
):
    """
    Get customers associated with the current logged-in user's workshop
    """
    workshop_id = get_current_user_workshop_id(current_user)
    result = await db.execute(
        select(models.Customer)
        .filter(models.Customer.workshop_id == workshop_id)
        .offset(skip)
        .limit(limit)
    )
    customers = result.scalars().all()
    return customers

async def create_current_user_workshop_customer(
    current_user: dict,
    customer: schemas.CustomerCreate,
    db: AsyncSession
):
    """
    Create a customer for the current logged-in user's workshop
    """
    workshop_id = get_current_user_workshop_id(current_user)
    create_customer_model = models.Customer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        phone=customer.phone,
        email=customer.email,
        workshop_id=workshop_id  # Set automatically from user's workshop
    )

    db.add(create_customer_model)
    await db.commit()
    await db.refresh(create_customer_model)
    return create_customer_model

async def patch_current_user_workshop_customer(
    current_user: dict,
    customer_id: int,
    customer_update: schemas.CustomerUpdate,
    db: AsyncSession
):
    """
    Update a customer for the current logged-in user's workshop
    """
    workshop_id = get_current_user_workshop_id(current_user)

    result = await db.execute(
        select(models.Customer).filter(
            models.Customer.customer_id == customer_id,
            models.Customer.workshop_id == workshop_id
        )
    )
    db_customer = result.scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)

    await db.commit()
    await db.refresh(db_customer)
    return db_customer

async def delete_current_user_workshop_customer(
    current_user: dict,
    customer_id: int,
    db: AsyncSession
):
    """
    Delete a customer for the current logged-in user's workshop
    """
    workshop_id = get_current_user_workshop_id(current_user)

    result = await db.execute(
        select(models.Customer).filter(
            models.Customer.customer_id == customer_id,
            models.Customer.workshop_id == workshop_id
        )
    )
    db_customer = result.scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    await db.execute(
        delete(models.Customer).where(models.Customer.customer_id == customer_id)
    )
    await db.commit()
    return db_customer
# ---------------- End of current user's workshop customers endpoint ----------------