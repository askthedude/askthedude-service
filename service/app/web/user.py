from fastapi import APIRouter

from dependencies.dependencies import GetUser, PostUser
from service.user_service import add_new_user, get_user_with_id

router = APIRouter()


@router.get("/user/{id}", response_model=GetUser)
async def get_user(id: int):
    return get_user_with_id(id)


@router.post("/user/", response_model=GetUser)
async def add_user(user: PostUser):
    return add_new_user(user)