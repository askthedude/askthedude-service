from service.exceptions.exceptions import ResourceNotFoundException, StorageFacadeException, ResourceConflictException, \
    ValidationException
from web.dto.dto import PostRole, UserFilter, AnonymousUserData, UserTechnologyInterestData
import service.user_service as service

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/user/")
async def filter_users(user_filter: UserFilter):
    try:
        return await service.filter_all_users(user_filter)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)


@router.get("/user/{id}")
async def get_user_profile(id: int):
    try:
        return await service.get_user_profile_with_id(id)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.errors)


@router.post("/role/")
async def add_user_role(role: PostRole):
    try:
        return await service.add_role(role)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)
    except ResourceConflictException as e:
        raise HTTPException(status_code=409, detail=e.errors)


@router.post("/user/anonymous")
async def add_user_device_token(user: AnonymousUserData):
    try:
        return await service.add_anonymous_user(user)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)


@router.post("/user/technology")
async def add_user_technology_interest(user_technology_data: UserTechnologyInterestData):
    try:
        return await service.add_user_technology_interest(user_technology_data)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)
