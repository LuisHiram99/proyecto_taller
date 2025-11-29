from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from auth.auth import get_current_user, pwd_context, admin_required, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from db import models, schemas
from exceptions.exceptions import notFoundException, fetchErrorException
from db.database import get_db

from ..workshops.service import get_current_user_workshop_id
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


# ---------------- Current user's workshop parts endpoint ----------------
async def create_current_user_workshop_part(
    current_user: dict,
    part: schemas.PartWorkshopCreate,
    db: AsyncSession
    ):
    """
    Create a part associated with the current logged-in user's workshop
    """
    workshop_id = get_current_user_workshop_id(current_user)
    
    # Check if this part already exists in the workshop
    existing_check = await db.execute(
        select(models.PartWorkshop)
        .filter(
            models.PartWorkshop.part_id == part.part_id,
            models.PartWorkshop.workshop_id == workshop_id
        )
    )
    existing_part = existing_check.scalar_one_or_none()
    
    if existing_part:
        raise HTTPException(
            status_code=400,
            detail=f"Part with ID {part.part_id} already exists in this workshop. Use PATCH to update it."
        )
    
    create_part_model = models.PartWorkshop(
        part_id=part.part_id,
        quantity=part.quantity,
        purchase_price=part.purchase_price,
        sale_price=part.sale_price,
        workshop_id=workshop_id  # Set automatically from user's workshop
    )

    db.add(create_part_model)
    await db.commit()
    await db.refresh(create_part_model)
    
    # Fetch the complete part data with join to return proper schema
    result = await db.execute(
        select(models.PartWorkshop, models.Part)
        .join(models.Part, models.PartWorkshop.part_id == models.Part.part_id)
        .filter(
            models.PartWorkshop.part_id == create_part_model.part_id,
            models.PartWorkshop.workshop_id == workshop_id
        )
    )
    part_workshop, part_data = result.first()
    
    # Combine data from both tables
    return schemas.PartWorkshop(
        part_id=part_workshop.part_id,
        workshop_id=part_workshop.workshop_id,
        quantity=part_workshop.quantity,
        purchase_price=part_workshop.purchase_price,
        sale_price=part_workshop.sale_price,
        part_name=part_data.part_name,
        brand=part_data.brand,
        description=part_data.description,
        category=part_data.category
    )

async def get_current_user_workshop_parts(
    current_user: dict,
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
):
    """
    Get parts associated with the current logged-in user's workshop
    """
    workshop_id = get_current_user_workshop_id(current_user)
    result = await db.execute(
        select(models.PartWorkshop, models.Part)
        .join(models.Part, models.PartWorkshop.part_id == models.Part.part_id)
        .filter(models.PartWorkshop.workshop_id == workshop_id)
        .offset(skip)
        .limit(limit)
    )
    parts_data = result.all()
    
    # Combine data from both tables
    return [
        schemas.PartWorkshop(
            part_id=part_workshop.part_id,
            workshop_id=part_workshop.workshop_id,
            quantity=part_workshop.quantity,
            purchase_price=part_workshop.purchase_price,
            sale_price=part_workshop.sale_price,
            part_name=part.part_name,
            brand=part.brand,
            description=part.description,
            category=part.category
        )
        for part_workshop, part in parts_data
    ]

async def update_current_user_workshop_part(
    current_user: dict,
    part_id: int,
    part_update: schemas.PartWorkshopUpdate,
    db: AsyncSession
):
    """
    Patch a part associated with the current logged-in user's workshop
    """
    workshop_id = get_current_user_workshop_id(current_user)

    result = await db.execute(
        select(models.PartWorkshop, models.Part)
        .join(models.Part, models.PartWorkshop.part_id == models.Part.part_id)
        .filter(
            models.PartWorkshop.part_id == part_id,
            models.PartWorkshop.workshop_id == workshop_id
        )
    )
    part_data = result.first()
    
    if not part_data:
        raise HTTPException(status_code=404, detail="Part not found in this workshop")
    
    part_workshop, part = part_data

    update_data = part_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(part_workshop, field, value)

    await db.commit()
    await db.refresh(part_workshop)

    return schemas.PartWorkshop(
        part_id=part_workshop.part_id,
        workshop_id=part_workshop.workshop_id,
        quantity=part_workshop.quantity,
        purchase_price=part_workshop.purchase_price,
        sale_price=part_workshop.sale_price,
        part_name=part.part_name,
        brand=part.brand,
        description=part.description,
        category=part.category
    )

async def delete_current_user_workshop_part(
    current_user: dict,
    part_id: int,
    db: AsyncSession
):
    """
    Delete a part associated with the current logged-in user's workshop
    """
    workshop_id = get_current_user_workshop_id(current_user)

    result = await db.execute(
        select(models.PartWorkshop, models.Part)
        .join(models.Part, models.PartWorkshop.part_id == models.Part.part_id)
        .filter(
            models.PartWorkshop.part_id == part_id,
            models.PartWorkshop.workshop_id == workshop_id
        )
    )
    part_data = result.first()
    
    if not part_data:
        raise HTTPException(status_code=404, detail="Part not found in this workshop")
    
    part_workshop, part = part_data

    await db.execute(
        delete(models.PartWorkshop).where(
            models.PartWorkshop.part_id == part_id,
            models.PartWorkshop.workshop_id == workshop_id
        )
    )
    await db.commit()
    
    return schemas.PartWorkshop(
        part_id=part_workshop.part_id,
        workshop_id=part_workshop.workshop_id,
        quantity=part_workshop.quantity,
        purchase_price=part_workshop.purchase_price,
        sale_price=part_workshop.sale_price,
        part_name=part.part_name,
        brand=part.brand,
        description=part.description,
        category=part.category
    )

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