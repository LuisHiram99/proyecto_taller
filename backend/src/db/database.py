from typing import Annotated
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query, Response
from typing import Any
from random import randint
from fastapi import Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

app = FastAPI(root_path="/api/v1")

# Construir DATABASE_URL desde variables de entorno
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
