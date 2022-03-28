from fastapi import APIRouter, HTTPException

from dependencies.dependencies import PostUser, PostProject
from service.service import add_new_user, get_user_with_id, add_new_project
from utils.log_config import LogConfig
from logging.config import dictConfig
import logging

dictConfig(LogConfig().dict())
logger = logging.getLogger("WEBAPI")


router = APIRouter()


@router.get("/user/{id}")
async def get_user(id: int):
    logger.info(f"Got HTTP GET request on URI: /user/{id}.")
    user = get_user_with_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.post("/user/")
async def add_user(user: PostUser):
    logger.info(f"Got HTTP POST request on URI: /user/. Body: {user}.")
    new_user = add_new_user(user)
    if new_user is None:
        raise HTTPException(status_code=409, detail="Couldn't add input user.")
    else:
        return new_user


@router.post("/project/")
async def add_project(project: PostProject):
    logger.info(f"Got HTTP POST request on URI: /project/. Body: {project}.")
    new_proj = add_new_project(project)
    if new_proj is None:
        raise HTTPException(status_code=409, detail="Couldn't add input proj.")
    else:
        return new_proj
