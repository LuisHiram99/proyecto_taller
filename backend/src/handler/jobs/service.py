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

# ---------------- BEGIN Jobs info functions ----------------
async def get_all_jobs_for_current_user_workshop(
        db: AsyncSession, 
        current_user: dict, 
        skip: int = 0, 
        limit: int = 100):
    '''
    Construct a query to get all jobs for the current user's workshop
    '''
    try:
        workshop_id = get_current_user_workshop_id(current_user)
        result = await db.execute(
            select(models.Job)
            .where(models.Job.workshop_id == workshop_id)
            .offset(skip)
            .limit(limit)
        )
        jobs = result.scalars().all()
        if not jobs:
            return []
        return jobs
    except Exception as e:
        print(f"Database error in get_all_jobs_for_current_user_workshop: {e}")
        raise fetchErrorException