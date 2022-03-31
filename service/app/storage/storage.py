from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .database import initialize_storage_development_mode
from .entity import User, Project, Technology, UserProjectAssociation, ProjectTechnologyAssociation
import datetime
import asyncio



class Storage():
    def __init__(self):
        async def init():
            await asyncio.run(initialize_storage_development_mode())
        init()

    async def get_uset_with_id(self, id: int, session: AsyncSession) -> Optional[User]:
        q = select(User).where(User.id == id)
        res = await session.execute(q)
        return res.first()


    async def get_uset_with_email(self, email: str, session: AsyncSession) -> Optional[User]:
        q = select(User).where(User.email == email)
        res = await session.execute(q)
        return res.first()

    def add_user_entity(self, user, session: AsyncSession) -> User:
        new_user = User(username=user.username, name=user.name,  email=user.email, github_url = user.github_url,
                        linkedin_url=user.linkedin_url, oauth=user.oauth_token)
        session.add(new_user)
        return new_user

    async def add_project_entity(self, project, session: AsyncSession):
        new_proj = Project(title=project.title, description=project.description, start_date=project.start_date,
                           stars=project.stars, url=project.url)
        await session.add(new_proj)
        return new_proj

    async def add_project_user_relation(self, project_id: int, user_id: int, session: AsyncSession):
        user_proj = UserProjectAssociation(project_id=project_id, user_id=user_id, create_time=datetime.datetime.now().isoformat())
        await session.add(user_proj)
        return user_proj

    async def add_project_technology_relation(self, project_id: int, tech_id: int, session: AsyncSession):
        proj_tech = ProjectTechnologyAssociation(project_id = project_id, technology_id = tech_id, create_time=datetime.datetime.now().isoformat())
        await session.add(proj_tech)
        return proj_tech

    async def add_technology(self, technology, session: AsyncSession):
        new_tech = Technology(name=technology.name, resource_url=technology.resource_url)
        await session.add(new_tech)
        return new_tech

    async def get_technologies_with_title(self, title: str, session: AsyncSession):
        return await session.query(Technology).filter(Technology.name == title)

    async def get_all_technologies(self, session: AsyncSession):
        return await session.query(Technology).all()

    async def filter_projects(self, project_filter, session: AsyncSession):
        # use project filter object
        return await session.query(Project).outerjoin(ProjectTechnologyAssociation, Project.technologies).outerjoin(Technology, Technology.projects).all()