from fastapi import APIRouter, HTTPException

from web.dto.dto import PostTechnology, TechnologyFilter
from service.technology_service import add_new_technology, filter_technologies

router = APIRouter()


@router.post("/technology/")
async def add_technology(technology: PostTechnology):
    new_tech = await add_new_technology(technology)
    if new_tech is None:
        raise HTTPException(status_code=409, detail="Couldn't add input technology.")
    else:
        return new_tech


@router.post("/technology/filter/")
async def filter_technology(technology_filter: TechnologyFilter):
    res = await filter_technologies(technology_filter)
    if res is None:
        raise HTTPException(status_code=403, detail="Couldn't find technologies technology.")
    else:
        return res
