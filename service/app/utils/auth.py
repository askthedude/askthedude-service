import bcrypt as bcrypt
import time
from typing import Dict
import jwt

from dependencies.config import settings


HASH_SALT_CONSTANT=10
JWT_TIMEOUT = 10000

HASHING_ERROR = "ERROR_HASH"


def get_hashed_password(plain_text_password):
    try:
        passwrd = plain_text_password.encode('utf-8')
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(passwrd, bcrypt.gensalt(HASH_SALT_CONSTANT)).decode('utf-8')
    except Exception as e:
        print(e)
        return HASHING_ERROR


def check_password(plain_text_password, hashed_password):
    try:
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(e)
        return False


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + JWT_TIMEOUT
    }
    try:
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    except Exception as e:
        print(e)
        return {}


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(e)
        return {}