import re
from utils.auth import get_hashed_password, check_password
from web.dto.dto import PostUser, SignInUser, GetUser

import storage.facade.user_storage_facade as user_facade
from utils.auth import signJWT


regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


async def add_new_user(user: PostUser):
    if re.fullmatch(regex, user.email):
        user.github_url="" #todo: temporary/ remove constraint on table of non null
        user.linkedin_url = "" #todo: temporary/ remove constraint on table of non null
        hashed_psswd = get_hashed_password(user.password)
        if hashed_psswd == "":
            return None
        user.password = hashed_psswd
        result = await user_facade.add_new_user(user)
        return {"token": signJWT(result.id), "user": result}
    else:
        print("Email not valid")
        return None


async def sign_in_user(user: SignInUser):
    res = await user_facade.get_user_profile_with_username(user.username)
    if res:
        res = res.User
        if check_password(user.password, res.hashed_password):
            user_data = GetUser(id=res.id, username=res.username, name=res.name, email=res.email, is_active=res.is_active,
                       github_url=res.github_url, linkedin_url=res.linkedin_url)
            return { "token": signJWT(res.id), "user": user_data}
        else:
            return None
    else:
        return None


