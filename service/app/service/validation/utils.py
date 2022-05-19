import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

PASSWORD_MIN_LENGTH = 5
COMMENT_MIN_LENGTH = 2

VALIDATION_ERROR_MESSAGES = {
    "username": "Username is missing.",
    "email": "Email is missing.",
    "email_format": "Email format is not correct.",
    "name": "Name is missing.",
    "password": "Password is missing.",
    "password_strength": f"Password too short. Please choose password of at least of length {PASSWORD_MIN_LENGTH}.",
    "title": "Project title is missing.",
    "technologies": "Technology id-s are missing for the project.",
    "technology_ids_invalid": "Specified technology ids are not valid.",
    "description": "Project description is missing.",
    "start_date": "Project start-date is missing.",
    "project": "Project with specified id is missing.",
    "project_missing": "Project id is missing from the subscription.",
    "subscriptions": "Number of subscription change is not valid.",
    "seen_frequency": "Number of seen frequency change is not valid.",
    "interested_num": "Number of interested people in project not valid.",
    "role": "Role title not specified.",
    "identifier_token": "identifier_token for anonymous user not present.",
    "identifier_token_user_missing": "User with identifier_token as specified couldn't be found.",
    "user":"User with specified id is not present.",
    "technology_name": "Technology name is missing.",
    "technology_url": "Technology url is missing.",
    "comment": f"Comment must be at least of length {COMMENT_MIN_LENGTH}."
}
