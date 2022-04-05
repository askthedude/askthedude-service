from typing import Optional, List
from dependencies.dependencies import storage
from dependencies.dependencies import PostProject, \
    GetProject, PostTechnology, GetTechnology, ProjectFilter
from storage.database import new_session


async def add_new_user_project_association_type(title: str):
    session = new_session()
    try:
        res = await storage.find_user_project_assoc_type_with_title(title, session)
        if res:
            return None
        else:
            storage.add_user_project_association_type_entity(title, session)
            await session.commit()
    except Exception as e:
        print(e)
        await session.rollback()
        return None
    finally:
        await session.close()


async def add_new_project(project: PostProject) -> Optional[GetProject]:
    session = new_session()
    try:
        proj = storage.add_project_entity(project, session)
        await session.flush()
        res = await storage.find_user_project_assoc_type_with_title("ADMIN", session)
        storage.add_project_user_relation(proj.id, project.user_id, res[0], session)
        for tech_id in project.technology_ids:
            storage.add_project_technology_relation(proj.id, tech_id, session)
        storage.add_blank_project_frequency_entity(proj.id, session)
        await session.commit()
        res = GetProject(id=proj.id, title=proj.title, description=proj.description, start_date=proj.start_date,
                          stars=proj.stars, github_url=proj.url, url=proj.url, is_active=proj.is_active, user_id=project.user_id,
                         technology_ids=project.technology_ids)
        return res
    except Exception as e:
        print(e)
        await session.rollback()
        return None
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


async def get_all_technologies() -> List[GetTechnology]:
    session = new_session()
    try:
        techs = await storage.get_all_technologies(session)
        return techs
    except Exception as e:
        print(e)
        return []
    finally:
        await session.close()


async def filter_projects(project_filter: ProjectFilter):
    session = new_session()
    try:
        res = await storage.filter_projects(project_filter, session)
        return res
    except Exception as e:
        print(e)
        return []
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

