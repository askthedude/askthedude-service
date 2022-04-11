from fastapi import APIRouter, HTTPException

from service.auth_service import add_new_user, sign_in_user
from web.dto.dto import PostUser, SignInUser

router = APIRouter()


@router.post("/signup/")
async def signup(user: PostUser):
    new_user = await add_new_user(user)
    if new_user is None:
        raise HTTPException(status_code=409, detail="Couldn't add input user.")
    else:
        return new_user


@router.post("/signin/")
async def signup(user: SignInUser):
    token = await sign_in_user(user)
    if token is None:
        raise HTTPException(status_code=401, detail="Couldn't sign in with input credentials.")
    else:
        return token