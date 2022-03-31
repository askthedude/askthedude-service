import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseSettings
import os


CONFIG_FOLDER_NAME='configuration'
CONFIG_FILE_NAME='.env'


class Settings(BaseSettings):
    # URL below might need to be changed from storage to localhost if
    # you only run storage in docker but are using local machine for service
    database_url: str = 'postgresql://postgres:postgres@storage'
    development_mode: bool = False

    class Config:
        env_file = os.path.join(os.path.dirname(__file__),'..',CONFIG_FOLDER_NAME,CONFIG_FILE_NAME)


settings = Settings()

engine = create_async_engine(
    settings.database_url,
    echo=True if settings.development_mode else False
)

new_session = sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        if settings.development_mode:
            print('dropping all')
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

init_db()