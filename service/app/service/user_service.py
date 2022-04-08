from typing import Optional
from web.dto.dto import UserFilter
from web.dto.dto import PostUser, GetUser, PostRole
from service.domain.domain import UserData, CompleteUserData, PartialProjectData

import storage.facade.user_storage_facade as user_facade


async def add_new_user(user: PostUser):
    result = await user_facade.add_new_user(user)
    return result


async def get_user_profile_with_id(id: int):
    user = await user_facade.get_user_profile_with_id(id)
    proj_result = []
    for proj in user.User.projects:
        temp_proj = PartialProjectData(proj.project.title, proj.project.description, proj.project.stars,
                                       proj.project.is_active, proj.project.id,
                                       proj.project.url, proj.project.url, [], [])
        proj_result.append(temp_proj)
    user_data = CompleteUserData(user.User.id, user.User.username, user.User.email, user.User.github_url, user.User.name,
                             user.User.is_active, user.User.linkedin_url, proj_result)
    return user_data


async def add_role(new_role: PostRole):
    result = await user_facade.add_role(new_role)
    return result


async def filter_all_users(user_filter: UserFilter):
    users = await user_facade.filter_all_users(user_filter)
    result = []
    for user in users:
        proj_result = []
        for proj in user.User.projects:
            temp_proj = PartialProjectData(proj.project.title, proj.project.description, proj.project.stars, proj.project.is_active, proj.project.id,
                               proj.project.url, proj.project.url,[], [])
            proj_result.append(temp_proj)
        user_data = CompleteUserData(user.User.id, user.User.username, user.User.email, user.User.github_url, user.User.name, user.User.is_active, user.User.linkedin_url, proj_result)
        result.append(user_data)
    return result
