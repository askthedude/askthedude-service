from typing import Optional, List
from dependencies.dependencies import storage
from dependencies.dependencies import PostUser, GetUser, PostProject, GetProject, PostTechnology, GetTechnology, ProjectFilter
from storage.database import new_session


async def add_new_user(user: PostUser) -> Optional[GetUser]:
    session = new_session()
    try:
        is_present = await _is_user_with_email_present(user.email, session)
        if is_present:
            return None
        user = storage.add_user_entity(user, session)
        await session.commit()
        await session.refresh(user)
        print(user.id)
        return GetUser(id=user.id, username=user.username, name=user.name, email=user.email, is_active=user.is_active,
                       github_url=user.github_url, linkedin_url=user.linkedin_url)
    except Exception as e:
        await session.rollback()
        return None


async def get_user_with_id(id: int) -> Optional[GetUser]:
    try:
        session = new_session()
        user = await storage.get_uset_with_id(id, session)
        if user:
            session.commit()
            return GetUser(id=user.id, name=user.name, username=user.username, email=user.email, is_active=user.is_active,
                           github_url=user.github_url, linkedin_url=user.linkedin_url)
        else:
            return None
    except Exception as e:
        print(e)
        return None


async def _is_user_with_email_present(email: str, session) -> bool:
    try:
        user = await storage.get_uset_with_email(email, session)
        return user is not None
    except Exception as e:
        print(e)
        return False


async def add_new_project(project: PostProject) -> Optional[GetProject]:
    try:
        session = await new_session()
        print("service started to insert")
        proj = await storage.add_project_entity(project, session)
        session.flush()
        print("added project entity")
        await storage.add_project_user_relation(proj.id, project.user_id, session)
        print("added project user relationship")
        for tech_id in project.technology_ids:
            await storage.add_project_technology_relation(proj.id, tech_id, session)
        print("Now going to commit")
        session.commit()
        print("committed")
        res = GetProject(id=proj.id, title=proj.title, description=proj.description, start_date=proj.start_date,
                          stars=proj.stars, github_url=proj.github_url, url=proj.url, is_active=proj.is_active)
        print(res)
        return res
    except Exception as e:
        print(e)
        return None


async def add_new_technology(technology: PostTechnology) -> Optional[GetTechnology]:
    try:
        session = await new_session()
        tech = await storage.add_technology(technology, session)
        session.commit()
        session.refresh(tech)
        return tech
    except Exception as e:
        print(e)
        return None


async def get_all_technologies() -> List[GetTechnology]:
    try:
        session = await new_session()
        techs = await storage.get_all_technologies(session)
        return techs
    except Exception as e:
        print(e)
        return []


async def filter_projects(project_filter: ProjectFilter):
    try:
        session = await new_session()
        return await storage.filter_projects(project_filter, session)
    except Exception as e:
        print(e)
        return []