from typing import List

from storage.facade.project_storage_facade import filter_technologies, get_project_by_id
from web.dto.dto import PostUser, SignInUser, PostProject, TechnologyFilter, ProjectSubscriptionData, \
    PostStatistics, PostRole, AnonymousUserData
from dataclasses import dataclass, field
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

VALIDATION_ERROR_MESSAGES = {
    "username": "Username is missing.",
    "email": "Email is missing.",
    "email_format": "Email format is not correct.",
    "name": "Name is missing.",
    "password": "Password is missing.",
    "password_strength": "Password too short. Please choose password of at least of length 5. )",
    "title": "Project title is missing",
    "technologies": "Technology id-s are missing for the project.",
    "technology_ids_invalid": "Specified technology ids are not valid",
    "description": "Project description is missing",
    "start_date": "Project start-date is missing",
    "project": "Project with specified id is missing",
    "project_missing": "Project id is missing from the subscription",
    "subscriptions": "Number of subscription change is not valid",
    "seen_frequency": "Number of seen frequency change is not valid",
    "interested_num": "Number of interested people in project not valid",
    "role": "Role title not specified",
    "identifier_token": "identifier_token for anonymous user not present."
}

PASSWORD_MIN_LENGTH = 5


@dataclass
class ValidationResult():
    valid: bool = True
    validationMessages: List[str] = field(default_factory=lambda: [])


def validate_add_user(user: PostUser) -> ValidationResult:
    result = ValidationResult()
    if user.username is None or user.username == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["username"])
    if user.email is None or user.email == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["email"])
    elif not re.fullmatch(regex, user.email):
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["email_format"])
    if user.name is None or user.name == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["name"])
    if user.password is None or user.password == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["password"])
    elif len(user.password) < PASSWORD_MIN_LENGTH:
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["password_strength"])
    return result


def validate_sign_in_user(user: SignInUser) -> ValidationResult:
    result = ValidationResult()
    if user.username is None or user.username == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["username"])
    if user.password is None or user.password == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["password"])
    return result


async def validate_new_project(project: PostProject) -> ValidationResult:
    result = ValidationResult()
    if project.title is None or project.title == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["title"])
    if project.technology_ids is None or len(project.technology_ids) == 0:
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["technologies"])
    technology_ids_valid = await _check_technology_ids_exist(project.technology_ids)
    if not technology_ids_valid:
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["technology_ids_invalid"])
    if project.description is None or project.description == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["description"])
    if project.start_date is None or project.start_date == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["start_date"])
    return result


async def _check_technology_ids_exist(technology_ids: List[int]) -> bool:
    try:
        technologies = await filter_technologies(TechnologyFilter())
        tech_set = {tech.Technology.id for tech in technologies}
        for id in technology_ids:
            if id not in tech_set:
                return False
        return True
    except Exception:
        return False


async def validate_project_subscription(subscription: ProjectSubscriptionData) -> ValidationResult:
    result = ValidationResult()
    if subscription.email is None or subscription.email == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["email"])
    if subscription.project_id is None or subscription.project_id < 0:
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["project_missing"])
    try:
        query_project = await get_project_by_id(subscription.project_id)
        if query_project is None:
            result.valid = False
            result.validationMessages.append(VALIDATION_ERROR_MESSAGES["project"])
    except Exception:
        result.valid = False
    return result


def validate_project_statistics(stats: PostStatistics) -> ValidationResult:
    result = ValidationResult()
    if stats.delta_subscriptions is not None and stats.delta_subscriptions < 0:
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["subscriptions"])
    if stats.delta_seen_frequency is not None and stats.delta_seen_frequency < 0:
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["seen_frequency"])
    if stats.delta_number_of_interested is not None and stats.delta_number_of_interested < 0:
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["interested_num"])
    return result


def validate_new_role(role: PostRole) -> ValidationResult:
    result = ValidationResult()
    if role.title is None or role.title == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["role"])
    return result


def validate_anonymous_user(user: AnonymousUserData) -> ValidationResult:
    result = ValidationResult()
    if user.identifier_token is None or user.identifier_token == "":
        result.valid = False
        result.validationMessages.append(VALIDATION_ERROR_MESSAGES["identifier_token"])
    return result