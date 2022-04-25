from starlette.requests import Request

from service.exceptions.exceptions import NotAuthorizedException
from utils.auth import decodeJWT

AUTH_HEADER_KEY = 'Authorization'
HEADER_SPLIT_TOKEN = " "
BEARER_TOKEN_DELIMITER = "Bearer:"
ID_KEY = "user_id"


def check_user_auth(request: Request):
    auth_header = request.headers.get(AUTH_HEADER_KEY)
    if auth_header:
        parts = auth_header.split(HEADER_SPLIT_TOKEN)
        if parts[0] == BEARER_TOKEN_DELIMITER:
            token = parts[1]
            result = decodeJWT(token)
            if bool(result) and ID_KEY in result:
                return result[ID_KEY]
    raise NotAuthorizedException("Couldn't get Bearer Auth token from the header of HTTP request.")
