from typing import Annotated
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query, Response
from typing import Any
from random import randint
from fastapi import Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


app = FastAPI(root_path="/api/v1")

DATABASE_URL = "postgresql+asyncpg://luishernandez:1234@localhost:5432/taller_db"

# Crea el motor
engine = create_async_engine(DATABASE_URL, echo=True)

# Crea una fábrica de sesiones
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Base para los modelos
Base = declarative_base()

# Dependency
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
