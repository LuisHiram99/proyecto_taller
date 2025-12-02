from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Annotated
from auth.auth import get_current_user, admin_required, pwd_context
from auth.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from . import service
from ..rate_limiter import limiter



from db import models, schemas
from db.database import get_db

router = APIRouter()

# ---------------- Workers endpoints ----------------
@router.get('/workers/', response_model=List[schemas.Worker])
async def read_workers(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    return await service.get_all_workers_for_current_user_workshop(db, current_user, skip, limit)

@router.post('/workers/', response_model=schemas.Worker)
async def create_worker(
    worker: schemas.WorkerCreateForWorkshop,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await service.add_worker_to_current_user_workshop(current_user, worker, db)
# ---------------- End of workers endpoints ----------------