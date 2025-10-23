from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session, engine, Base
from models import Usuario
from sqlalchemy import text

app = FastAPI()

# Dependencia para obtener sesión
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.on_event("startup")
async def startup():
    # Crea tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "API del taller conectada con PostgreSQL"}

@app.get("/usuarios")
async def get_usuarios(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT * FROM usuarios"))
    usuarios = result.mappings().all()
    return {"usuarios": usuarios}