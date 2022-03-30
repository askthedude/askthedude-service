from typing import Optional, List

from sqlalchemy.orm import Session

from dependencies.dependencies import storage
from dependencies.dependencies import PostUser, GetUser, PostProject, GetProject, PostTechnology, GetTechnology, ProjectFilter
from storage.database import new_session


async def add_new_user(user: PostUser) -> Optional[GetUser]:
    try:
        session = new_session()
        is_present = await _is_user_with_email_present(user.email, session)
        if is_present:
            return None
        user = storage.add_user_entity(user, session)
        session.commit()
        session.refresh(user)
        return GetUser(id=user.id, username=user.username, name=user.name, email=user.email, is_active=user.is_active,
                       github_url=user.github_url, linkedin_url=user.linkedin_url)
    except Exception:
        return None


async def get_user_with_id(id: int) -> Optional[GetUser]:
    try:
        session = new_session()
        user = storage.get_uset_with_id(id, session)
        if user:
            session.commit()
            return GetUser(id=user.id, name=user.name, username=user.username, email=user.email, is_active=user.is_active,
                           github_url=user.github_url, linkedin_url=user.linkedin_url)
        else:
            return None
    except Exception:
        return None


async def _is_user_with_email_present(email: str, session: Session) -> bool:
    try:
        user = storage.get_uset_with_email(email, session)
        return user is not None
    except Exception:
        return False


async def add_new_project(project: PostProject) -> Optional[GetProject]:
    try:
        session = new_session()
        proj = storage.add_project_entity(project, session)
        storage.add_project_user_relation(proj.id, project.user_id, session)
        for tech_id in project.technology_ids:
            storage.add_project_technology_relation(proj.id, tech_id, session)
        session.commit()
        session.refresh(proj)
        return GetProject(id=proj.id, title=proj.title, description=proj.description, start_date=proj.start_date,
                          stars=proj.stars, github_url=proj.github_url, url=proj.url, is_active=proj.is_active)
    except Exception:
        return None


async def add_new_technology(technology: PostTechnology) -> Optional[GetTechnology]:
    try:
        session = new_session()
        tech = storage.add_technology(technology, session)
        session.commit()
        session.refresh(tech)
    except Exception:
        return None


async def get_all_technologies() -> List[GetTechnology]:
    try:
        session = new_session()
        techs = storage.get_all_technologies(session)
        return techs
    except Exception:
        return []


async def filter_projects(project_filter: ProjectFilter):
    try:
        session = new_session()
        return storage.filter_projects(project_filter, session)
    except Exception:
        return []