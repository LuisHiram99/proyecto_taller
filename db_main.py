from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.db.database import async_session, engine, Base
from models import Usuario
from sqlalchemy import text
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al iniciar la app
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # liberar recursos si fuera necesario

app = FastAPI(lifespan=lifespan, root_path="/api/v1")

async def get_session():
    async with async_session() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "API del taller conectada con PostgreSQL"}

@app.get("/usuarios")
async def get_usuarios(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT * FROM usuarios"))
    usuarios = result.mappings().all()
    return {"usuarios": usuarios}