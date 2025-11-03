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
@router.post("/workshop/", response_model=schemas.Workshop, summary="Create workshop for current user")
async def create_current_user_workshop(
    user: user_dependency,
    workshop: schemas.WorkshopCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a workshop associated with the currently authenticated user
    """

    if get_current_user_workshop_id(user) is not 1:
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
        select(models.User).filter(models.User.user_id == user["user_id"])
    )
    db_user = result.scalar_one_or_none()
    db_user.workshop_id = create_workshop_model.workshop_id
    await db.commit()
    await db.refresh(db_user)

    return create_workshop_model

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

@router.put("/workshop/", response_model=schemas.Workshop, summary="Update current user's workshop")
async def update_current_user_workshop(
    user: user_dependency,
    workshop: schemas.WorkshopUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update the workshop associated with the currently authenticated user
    """
    if get_current_user_workshop_id(user) is 1:
        raise HTTPException(status_code=400, detail="User has no workshop to update")

    result = await db.execute(
        select(models.Workshop).filter(models.Workshop.workshop_id == user["workshop_id"])
    )
    db_workshop = result.scalar_one_or_none()
    if db_workshop is None:
        raise HTTPException(status_code=404, detail="Workshop not found")

    update_data = workshop.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_workshop, field, value)

    await db.commit()
    await db.refresh(db_workshop)
    return db_workshop

# ---------------- End of current user's workshop related functions ----------------


# ---------------- Current user's workshop customers endpoint ----------------

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

@router.post("/workshop/customers/", response_model=schemas.Customer, summary="Create customer for current user's workshop")
async def create_current_user_workshop_customer(
    user: user_dependency,
    customer: schemas.CustomerCreateForWorkshop,  # Changed this
    db: AsyncSession = Depends(get_db)
):
    """
    Create a customer associated with the currently authenticated user's workshop
    """
    workshop_id = get_current_user_workshop_id(user)

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

@router.put("/workshop/customers/{customer_id}", response_model=schemas.Customer, summary="Update customer of current user's workshop")
async def update_current_user_workshop_customer(
    user: user_dependency,
    customer_id: int,
    customer: schemas.CustomerUpdateForWorkshop,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a customer associated with the currently authenticated user's workshop
    """
    workshop_id = get_current_user_workshop_id(user)

    result = await db.execute(
        select(models.Customer).filter(
            models.Customer.customer_id == customer_id,
            models.Customer.workshop_id == workshop_id
        )
    )
    db_customer = result.scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)

    await db.commit()
    await db.refresh(db_customer)
    return db_customer


@router.delete("/workshop/customers/{customer_id}", response_model=schemas.Customer, summary="Delete customer of current user's workshop")
async def delete_current_user_workshop_customer(
    user: user_dependency,
    customer_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a customer associated with the currently authenticated user's workshop
    """
    workshop_id = get_current_user_workshop_id(user)

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


def get_current_user_workshop_id(user: dict) -> int:
    """
    Utility function to get the workshop ID of the current user
    """
    return user.get("workshop_id")

