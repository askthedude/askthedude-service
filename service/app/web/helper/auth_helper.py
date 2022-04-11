from starlette.requests import Request
from utils.auth import decodeJWT


def check_user_auth(request: Request):
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    if auth_header:
        parts = auth_header.split(" ")
        print(parts)
        if parts[0] == 'Bearer:':
            token = parts[1]
            print(token)
            result = decodeJWT(token)
            print(result)
            if bool(result):
                return result['user_id']
            else:
                return None
        else:
            return None
    else:
        return None
