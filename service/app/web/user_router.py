from web.dto.dto import PostRole, UserFilter
from service.user_service import  \
    get_user_profile_with_id, add_role, filter_all_users

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
