from fastapi import APIRouter, HTTPException

from dependencies.dependencies import PostUser, PostProject, PostTechnology, ProjectFilter
from service.service import add_new_user, get_user_with_id, add_new_project, add_new_technology, filter_projects

router = APIRouter()


@router.get("/user/{id}")
async def get_user(id: int):
    user = await get_user_with_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.post("/user/")
async def add_user(user: PostUser):
    new_user = await add_new_user(user)
    if new_user is None:
        raise HTTPException(status_code=409, detail="Couldn't add input user.")
    else:
        return new_user


@router.post("/project/")
async def add_project(project: PostProject):
    new_proj = await add_new_project(project)
    if new_proj is None:
        raise HTTPException(status_code=409, detail="Couldn't add input project.")
    else:
        return new_proj


@router.post("/technology/")
async def add_technology(technology: PostTechnology):
    new_tech = await add_new_technology(technology)
    if new_tech is None:
        raise HTTPException(status_code=409, detail="Couldn't add input technology.")
    else:
        return new_tech


@router.get("/project")
async def filter_query_projects(project_filter: ProjectFilter):
    res = await filter_projects(project_filter)
    return res