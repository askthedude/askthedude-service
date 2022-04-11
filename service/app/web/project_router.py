from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from web.dto.dto import PostProject, PostTechnology, ProjectFilter, PostStatistics
from service.project_service import add_new_project, add_new_technology, \
    search_projects, get_project_by_id, post_project_statistics
from web.helper.auth_helper import check_user_auth

router = APIRouter()


@router.post("/project/")
async def add_project(project: PostProject, request: Request):
    user_id = check_user_auth(request)
    if user_id is not None:
        new_proj = await add_new_project(project, user_id)
        if new_proj is None:
            raise HTTPException(status_code=409, detail="Couldn't add input project.")
        else:
            return new_proj
    else:
        raise HTTPException(status_code=403, detail="Couldn't authorize for project addition.")


@router.post("/technology/")
async def add_technology(technology: PostTechnology):
    new_tech = await add_new_technology(technology)
    if new_tech is None:
        raise HTTPException(status_code=409, detail="Couldn't add input technology.")
    else:
        return new_tech


@router.post("/project/filter")
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


@router.post("/project/{id}/stats")
async def update_project_statistics(id: int, stats: PostStatistics):
    res = await post_project_statistics(id, stats)
    if res is None:
        raise HTTPException(status_code=409, detail="Couldn't Update project statistics.")
    else:
        return res