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

router = APIRouter(tags=["workers"])

user_dependency = Annotated[dict, Depends(get_current_user)]

# ---------------- Current user's info endpoints ----------------
