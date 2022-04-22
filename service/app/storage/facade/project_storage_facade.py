from typing import Optional, List

from web.dto.dto import ProjectFilter, PostProject, \
    GetProject, PostTechnology, GetTechnology, PostStatistics, TechnologyFilter, \
    ProjectSubscriptionData
from storage.database import new_session
from storage.storage import storage


async def add_new_project(project: PostProject, user_id: int) -> Optional[GetProject]:
    session = new_session()
    try:
        proj = storage.add_project_entity(project, session)
        await session.flush()
        res = await storage.find_user_project_assoc_type_with_title("ADMIN", session)
        storage.add_project_user_relation(proj.id, user_id, res[0], session)
        for tech_id in project.technology_ids:
            storage.add_project_technology_relation(proj.id, tech_id, session)
        storage.add_blank_project_frequency_entity(proj.id, session)
        await session.commit()
        res = GetProject(id=proj.id, title=proj.title, description=proj.description, start_date=proj.start_date,
                          stars=proj.stars, github_url=proj.url, url=proj.url, is_active=proj.is_active, user_id=user_id,
                         technology_ids=project.technology_ids)
        return res
    except Exception as e:
        print(e)
        await session.rollback()
        return None
    finally:
        await session.close()


async def filter_projects(project_filter: ProjectFilter):
    session = new_session()
    try:
        projects = await storage.filter_projects(project_filter, session)
        return projects
    except Exception as e:
        print(e)
        return []
    finally:
        await session.close()


async def add_new_technology(technology: PostTechnology) -> Optional[GetTechnology]:
    session = new_session()
    try:
        tech = storage.add_technology(technology, session)
        await session.commit()
        await session.refresh(tech)
        return tech
    except Exception as e:
        await session.rollback()
        print(e)
        return None
    finally:
        await session.close()


async def add_new_subscription_project(subscription: ProjectSubscriptionData):
    session = new_session()
    try:
        new_subscription = storage.add_subscription(subscription, session)
        await session.commit()
        await session.refresh(new_subscription)
        return new_subscription
    except Exception as e:
        await session.rollback()
        print(e)
        return None
    finally:
        await session.close()


async def get_project_by_id(id: int):
    session = new_session()
    try:
        res = await storage.get_project_by_id(id, session)
        return res
    except Exception as e:
        print(e)
        return None
    finally:
        await session.close()


async def filter_technologies(tech_filter: TechnologyFilter):
    session = new_session()
    try:
        techs = await storage.filter_technologies(tech_filter.title, session)
        return techs
    except Exception as e:
        print(e)
        return []
    finally:
        await session.close()


async def update_project_stats(id: int, stats: PostStatistics):
    session = new_session()
    try:
        techs = await storage.update_project_stats(id, stats, session)
        await session.commit()
        return techs
    except Exception as e:
        await session.rollback()
        print(e)
        return []
    finally:
        await session.close()