import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from db.database import Base
from db import models  # Import all models to ensure they're registered
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from config/.env
env_path = Path(__file__).parent.parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

# Build test database URL from environment variables
DB_USER = os.getenv("DB_USER", "luishernandez")
DB_PASSWORD = os.getenv("DB_PASSWORD", "luishernandez")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME_TEST = os.getenv("DB_NAME_TEST", "talleres_test_db")  # Use separate test DB name

TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_TEST}"


@pytest_asyncio.fixture(scope="function")
async def async_engine():
    """Create a test database engine with schema from models"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False
    )
    
    # Create all tables from Base.metadata (matches your models exactly)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
        # Create enums (they get dropped with CASCADE above, so safe to recreate)
        await conn.execute(text("CREATE TYPE role_enum AS ENUM ('admin', 'manager', 'worker')"))
        await conn.execute(text("CREATE TYPE status_enum AS ENUM ('pending', 'in_progress', 'completed')"))
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup after tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("DROP TYPE IF EXISTS role_enum CASCADE"))
        await conn.execute(text("DROP TYPE IF EXISTS status_enum CASCADE"))
    
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session(async_engine):
    """Create a test database session factory"""
    async_session_maker = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    return async_session_maker


@pytest_asyncio.fixture(scope="function")
async def db_session(async_session):
    """Provide a transactional scope for tests with default workshop"""
    async with async_session() as session:
        # Create default workshop for foreign key constraints
        default_workshop = models.Workshop(
            workshop_id=1,
            workshop_name="Test Workshop",
            address="123 Test St",
            opening_hours="09:00",
            closing_hours="18:00"
        )
        session.add(default_workshop)
        await session.commit()
        
        yield session
        await session.rollback()
