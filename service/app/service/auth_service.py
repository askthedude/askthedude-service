import time
from typing import Dict
import jwt
import re

from dependencies.config import settings
from utils.auth import get_hashed_password, check_password
from web.dto.dto import PostUser, SignInUser
import storage.facade.user_storage_facade as user_facade


JWT_TIMEOUT = 100


regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


async def add_new_user(user: PostUser):
    if re.fullmatch(regex, user.email):
        hashed_psswd = get_hashed_password(user.password)
        if hashed_psswd == "":
            return None
        user.password = hashed_psswd
        result = await user_facade.add_new_user(user)
        return {"token": signJWT(result.User.id)}
    else:
        print("Email not valid")
        return None


async def sign_in_user(user: SignInUser):
    user_data = await user_facade.get_user_profile_with_username(user.username)
    if user_data:
        if check_password(user.password, user_data.User.hashed_password):
            return { "token": signJWT(user_data.User.id)}
        else:
            return None
    else:
        return None


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + JWT_TIMEOUT
    }
    try:
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    except Exception as e:
        print(e)
        return {}


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(e)
        return {}