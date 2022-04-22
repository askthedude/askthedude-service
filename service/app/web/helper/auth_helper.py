from starlette.requests import Request
from utils.auth import decodeJWT


def check_user_auth(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        parts = auth_header.split(" ")
        if parts[0] == 'Bearer:':
            token = parts[1]
            result = decodeJWT(token)
            if bool(result):
                return result['user_id']
            else:
                return None
        else:
            return None
    else:
        return None
