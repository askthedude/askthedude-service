from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.config import database_url, settings


engine = create_async_engine(
    database_url,
    echo=True if settings.development_mode else False
)

new_session = sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
