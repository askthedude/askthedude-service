from fastapi import APIRouter, HTTPException

import service.auth_service as service
from service.exceptions.exceptions import ValidationException, CryptoException, StorageFacadeException, \
    FailedLoginException
from web.dto.dto import PostUser, SignInUser

router = APIRouter()


@router.post("/signup/")
async def signup(user: PostUser):
    try:
        return await service.add_new_user(user)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except CryptoException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)


@router.post("/signin/")
async def signup(user: SignInUser):
    try:
        return await service.sign_in_user(user)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except FailedLoginException as e:
        raise HTTPException(status_code=401, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)