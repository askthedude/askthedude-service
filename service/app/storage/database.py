import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.config import settings


engine = create_async_engine(
    settings.database_url,
    echo=True if settings.development_mode else False
)

new_session = sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        if settings.development_mode and settings.drop_recreate_tables:
            print("Dropping tables and recreating them")
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
