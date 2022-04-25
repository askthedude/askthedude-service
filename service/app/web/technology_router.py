from fastapi import APIRouter, HTTPException

from service.exceptions.exceptions import ValidationException, StorageFacadeException
from web.dto.dto import PostTechnology, TechnologyFilter
from service.technology_service import add_new_technology, filter_technologies

router = APIRouter()


@router.post("/technology/")
async def add_technology(technology: PostTechnology):
    try:
        return await add_new_technology(technology)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.errors)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)


@router.post("/technology/filter/")
async def filter_technology(technology_filter: TechnologyFilter):
    try:
        return await filter_technologies(technology_filter)
    except StorageFacadeException as e:
        raise HTTPException(status_code=503, detail=e.errors)