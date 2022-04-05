from fastapi import APIRouter, HTTPException

from dependencies.dependencies import PostProject, PostTechnology, ProjectFilter
from service.project_service import add_new_project, add_new_technology, \
    search_projects, get_project_by_id

router = APIRouter()


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


@router.get("/project/")
async def filter_query_projects(project_filter: ProjectFilter):
    res = await search_projects(project_filter)
    return res


@router.get("/project/{id}")
async def filter_query_projects(id: int):
    res = await get_project_by_id(id)
    if res is None:
        raise HTTPException(status_code=404, detail="Couldn't find project with specified id.")
    else:
        return res