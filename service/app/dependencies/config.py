from typing import Optional

from pydantic import BaseSettings
import os


CONFIG_FOLDER_NAME='configuration'
CONFIG_FILE_NAME='.env'


class Settings(BaseSettings):
    # URL below might need to be changed from storage to localhost if
    # you only run storage in docker but are using local machine for service
    DATABASE_HOST_URL: str = ""
    DATABASE_USER: str = ""
    DATABASE_PASSWORD: str = ""
    development_mode: bool = False
    drop_recreate_tables: bool = False
    JWT_SECRET: str
    JWT_ALGORITHM: str
    class Config:
        env_file = os.path.join(os.path.dirname(__file__),'..',CONFIG_FOLDER_NAME,CONFIG_FILE_NAME)


settings = Settings()
database_url: str = f'postgresql+asyncpg://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST_URL}'