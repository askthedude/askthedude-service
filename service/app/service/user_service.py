from service.exceptions.exceptions import ResourceNotFoundException, ValidationException
from service.validation.validation import validate_new_role, ValidationResult, validate_anonymous_user, \
    validate_user_technology_interest
from web.dto.dto import UserFilter, PostRole, AnonymousUserData, UserTechnologyInterestData
from service.domain.domain import CompleteUserData, PartialProjectData, AnonymousUser, UserTechnologyInterest

import storage.facade.user_storage_facade as user_facade


async def get_user_profile_with_id(id: int):
    user = await user_facade.get_user_profile_with_id(id)
    if user is None:
        raise ResourceNotFoundException(f"Couldn't find user with specified id of: {id}")
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
    validation_res :ValidationResult = validate_new_role(new_role)
    if validation_res.valid:
        return await user_facade.add_role(new_role)
    else:
        raise ValidationException("New input Role is not valid", validation_res.validationMessages)


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


async def add_anonymous_user(user: AnonymousUserData):
    validation_res: ValidationResult = validate_anonymous_user(user)
    if validation_res.valid:
        return await user_facade.add_anonymous_user(user)
    else:
        raise ValidationException("Anonymous user data not valid", validation_res.validationMessages)


async def add_user_technology_interest(user_technology: UserTechnologyInterestData):
    validation_res: ValidationResult = await validate_user_technology_interest(user_technology)
    if validation_res.valid:
        anonymous_user = await user_facade.get_user_with_identifier_token(user_technology.user_identifier_token)
        interests = []
        for technology_id in user_technology.technology_ids:
            user_tech = UserTechnologyInterest(technology_id, anonymous_user.User.id)
            new_interest = await user_facade.add_user_technology_interest(user_tech)
            interests.append(new_interest)
        return interests
    else:
        raise ValidationException("Anonymous user data not valid", validation_res.validationMessages)
