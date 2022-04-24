from service.exceptions.exceptions import ValidationException, CryptoException, FailedLoginException
from service.validation.validation import validate_add_user, ValidationResult, validate_sign_in_user
from utils.auth import get_hashed_password, check_password, HASHING_ERROR
from web.dto.dto import PostUser, SignInUser, GetUser

import storage.facade.user_storage_facade as user_facade
from utils.auth import signJWT


async def add_new_user(user: PostUser):
    validation_result: ValidationResult = validate_add_user(user)
    print(validation_result)
    if validation_result.valid:
        hashed_psswd = get_hashed_password(user.password)
        if hashed_psswd == HASHING_ERROR:
            raise CryptoException("Error while trying to hash input password", "Couldn't hash password")
        user.password = hashed_psswd
        result = await user_facade.add_new_user(user)
        return {"token": signJWT(result.id), "user": result}
    else:
        raise ValidationException("Add User Validation failed", validation_result.validationMessages)


async def sign_in_user(user: SignInUser):
    validation_result: ValidationResult = validate_sign_in_user(user)
    if validation_result.valid:
        query_user = await user_facade.get_user_profile_with_username(user.username)
        if query_user is None:
            raise FailedLoginException("Couldn't find user with specified username.")
        query_user = query_user.User
        if check_password(user.password, query_user.hashed_password):
            user_data = GetUser(id=query_user.id, username=query_user.username, name=query_user.name, email=query_user.email,
                                is_active=query_user.is_active,
                                github_url=query_user.github_url, linkedin_url=query_user.linkedin_url)
            return {"token": signJWT(query_user.id), "user": user_data}
        else:
            raise FailedLoginException("Couldn't login with username and password.")
    else:
        raise ValidationException("Sign in Validation failed", validation_result.validationMessages)


