from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from auth.auth import get_current_user, pwd_context, admin_required, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from db import models, schemas
from exceptions.exceptions import notFoundException, fetchErrorException
from db.database import get_db

from ..workshops.service import get_current_user_workshop_id

from db import models, schemas
from db.database import get_db

router = APIRouter(tags=["workers"])


# ---------------- BEGIN Current user's info functions ----------------
async def add_worker_to_current_user_workshop(
    current_user: dict,
    worker: schemas.WorkerCreateForWorkshop,
    db: AsyncSession
):
    """
    Add a worker to the current logged-in user's workshop
    """
    workshop_id = get_current_user_workshop_id(current_user)
    create_worker_model = models.Worker(
        first_name=worker.first_name,
        last_name=worker.last_name,
        nickname=worker.nickname,
        phone=worker.phone,
        position=worker.position,
        workshop_id=workshop_id  # Set automatically from user's workshop
    )

    db.add(create_worker_model)
    await db.commit()
    await db.refresh(create_worker_model)
    return create_worker_model

async def get_all_workers_for_current_user_workshop(
        db: AsyncSession, 
        current_user: dict, 
        skip: int = 0, 
        limit: int = 100):
    '''
    Construct a query to get all workers for the current user's workshop
    '''
    try:
        workshop_id = get_current_user_workshop_id(current_user)
        result = await db.execute(
            select(models.Worker)
            .where(models.Worker.workshop_id == workshop_id)
            .offset(skip)
            .limit(limit)
        )
        workers = result.scalars().all()
        if not workers:
            raise notFoundException
        return workers
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in get_all_workers_for_current_user_workshop: {e}")
        raise fetchErrorException

# ---------------- END Current user's info functions ----------------


