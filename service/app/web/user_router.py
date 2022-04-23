from web.dto.dto import PostRole, UserFilter, AnonymousUserData
from service.user_service import  \
    get_user_profile_with_id, add_role, filter_all_users, add_anonymous_user

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/user/")
async def filter_users(user_filter: UserFilter):
    users = await filter_all_users(user_filter)
    if users is None:
        raise HTTPException(status_code=404, detail="Users with applied filter not found")
    else:
        return users


@router.get("/user/{id}")
async def get_user_profile(id: int):
    user = await get_user_profile_with_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.post("/role/")
async def add_user_role(role: PostRole):
    new_role = await add_role(role)
    if new_role is None:
        raise HTTPException(status_code=409, detail="Couldn't add input role.")
    else:
        return new_role


@router.post("/user/anonymous")
async def add_user_device_token(user: AnonymousUserData):
    new_anonymous_user = await add_anonymous_user(user)
    if new_anonymous_user is None:
        raise HTTPException(status_code=409, detail="Couldn't add new anonymous user.")
    else:
        return new_anonymous_user
