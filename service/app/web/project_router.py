from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from service.exceptions.exceptions import ValidationException, NotAuthorizedException, StorageFacadeException, \
    ResourceNotFoundException
from web.dto.dto import PostProject, ProjectFilter, PostStatistics, ProjectSubscriptionData, AddCommentDto
from service.project_service import add_new_project, \
    search_projects, get_project_by_id, post_project_statistics, add_new_subscription_for_project, \
    add_comment_to_project
from web.helper.auth_helper import check_user_auth

router = APIRouter()


@router.post("/project/")
async def add_project(project: PostProject, request: Request):
    try:
        user_id = check_user_auth(request)
        return await add_new_project(project, user_id)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except NotAuthorizedException as e:
        raise HTTPException(status_code=401, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)


@router.post("/project/filter")
async def filter_query_projects(project_filter: ProjectFilter):
    try:
        return await search_projects(project_filter)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)


@router.post("/project/subscription")
async def add_project_subscription(project_subscription: ProjectSubscriptionData):
    try:
        return await add_new_subscription_for_project(project_subscription)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)


@router.get("/project/{id}")
async def query_project(id: int):
    try:
        return await get_project_by_id(id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)


@router.post("/project/{id}/stats")
async def update_project_statistics(id: int, stats: PostStatistics):
    try:
        return await post_project_statistics(id, stats)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)


@router.post("/project/comment")
async def add_comment(addComment: AddCommentDto):
    try:
        return await add_comment_to_project(addComment)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)
