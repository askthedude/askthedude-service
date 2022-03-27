from fastapi import FastAPI
import web.user as user_router

from storage.entity import User, Project, Technology, Base
from storage.database import SessionLocal, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.router)