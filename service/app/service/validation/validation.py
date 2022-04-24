from typing import List

from web.dto.dto import PostUser, SignInUser
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
