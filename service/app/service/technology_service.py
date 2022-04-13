from typing import List, Optional

import storage.facade.project_storage_facade as project_facade

from web.dto.dto import GetTechnology, PostTechnology, TechnologyFilter


async def add_new_technology(technology: PostTechnology) -> Optional[GetTechnology]:
    result = await project_facade.add_new_technology(technology)
    return result


async def filter_technologies(tech_filter: TechnologyFilter) -> List[GetTechnology]:
    result = await project_facade.filter_technologies(tech_filter)
    techs = [GetTechnology(id=x.Technology.id, name=x.Technology.name,
                           resource_url=x.Technology.resource_url, is_hot=x.Technology.is_hot) for x in result]
    return techs
