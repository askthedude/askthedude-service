from typing import Optional

from sqlalchemy import select, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, contains_eager, subqueryload

from .entity import User, Project, Technology, UserProjectAssociation, \
    ProjectTechnologyAssociation, Role, UserRoleAssociation, UserProjectAssociationType, \
    ProjectStatistics

import datetime


class Storage():
    async def get_uset_with_id(self, id: int, session: AsyncSession) -> Optional[User]:
        q = select(User).filter(User.id == id)
        res = await session.execute(q)
        return res.first()

    async def get_uset_with_email(self, email: str, session: AsyncSession) -> Optional[User]:
        q = select(User).filter(User.email == email)
        res = await session.execute(q)
        return res.first()

    def add_user_entity(self, user, session: AsyncSession) -> User:
        new_user = User(username=user.username, name=user.name,  email=user.email, github_url = user.github_url,
                        linkedin_url=user.linkedin_url, oauth=user.oauth_token)
        session.add(new_user)
        return new_user

    def add_project_entity(self, project, session: AsyncSession):
        new_proj = Project(title=project.title, description=project.description, start_date=project.start_date,
                           stars=project.stars, url=project.url)
        session.add(new_proj)
        return new_proj

    def add_project_user_relation(self, project_id: int, user_id: int, proj_user_rel_type_id: int,  session: AsyncSession):
        user_proj = UserProjectAssociation(project_id=project_id, user_id=user_id, create_time=datetime.datetime.now().isoformat(), type_id=proj_user_rel_type_id)
        session.add(user_proj)
        return user_proj

    def add_project_technology_relation(self, project_id: int, tech_id: int, session: AsyncSession):
        proj_tech = ProjectTechnologyAssociation(project_id = project_id, technology_id = tech_id, create_time=datetime.datetime.now().isoformat())
        session.add(proj_tech)
        return proj_tech

    def add_technology(self, technology, session: AsyncSession):
        new_tech = Technology(name=technology.name, resource_url=technology.resource_url, is_hot=False)
        session.add(new_tech)
        return new_tech

    def add_user_project_association_type_entity(self, title: str, session: AsyncSession):
        entity = UserProjectAssociationType(title=title)
        session.add(entity)
        return entity

    async def find_user_project_assoc_type_with_title(self, title: str, session: AsyncSession):
        q = select(UserProjectAssociationType.id)\
            .filter(UserProjectAssociationType.title == title)
        res = await session.execute(q)
        return res.first()

    def add_blank_project_frequency_entity(self, project_id: int, session: AsyncSession):
        entity = ProjectStatistics(project_id=project_id)
        session.add(entity)
        return entity

    async def get_technologies_with_title(self, title: str, session: AsyncSession):
        q = select(Technology).filter(Technology.name == title)
        res = await session.execute(q)
        return res.all()

    async def get_all_technologies(self, session: AsyncSession):
        q = select(Technology)
        res = await session.execute(q)
        return res.all()

    async def filter_projects(self, project_filter, session: AsyncSession):
        q = select(Project) \
            .options(subqueryload(Project.technologies).subqueryload(ProjectTechnologyAssociation.technology)) \
            .options(subqueryload(Project.users).subqueryload(UserProjectAssociation.user))\
            .options(subqueryload(Project.users).subqueryload(UserProjectAssociation.type))\
            .filter(Project.title.like('%'+project_filter.title+'%'))\
            .filter(Project.description.like('%'+project_filter.description+'%'))\
            .filter(Project.is_active == project_filter.is_active) \
            .filter(UserProjectAssociationType.title == 'ADMIN') \
            .limit(project_filter.limit) \
            .offset(project_filter.offset)
        res = await session.execute(q)
        return res.all()

    async def get_project_by_id(self, id: int, session: AsyncSession):
        q = select(Project) \
            .options(subqueryload(Project.technologies).subqueryload(ProjectTechnologyAssociation.technology)) \
            .options(subqueryload(Project.users).subqueryload(UserProjectAssociation.user)) \
            .options(subqueryload(Project.statistics)) \
        .filter(Project.id == id)
        res = await session.execute(q)
        return res.first()

    def add_role_entity(self, role, session: AsyncSession):
        role = Role(title=role.title)
        session.add(role)
        return role

    def add_user_role_entity(self, user_id: int, role_id: int, session: AsyncSession):
        user_role = UserRoleAssociation(user_id=user_id, role_id=role_id)
        session.add(user_role)
        return user_role

    async def get_role_with_title(self, title: str, session: AsyncSession):
        q = select(Role).filter(Role.title == title)
        res = await session.execute(q)
        return res.first()

    async def filter_users(self, user_filter, session: AsyncSession):
        q = select(User)\
            .options(subqueryload(User.projects).subqueryload(UserProjectAssociation.project)) \
            .filter(User.name.like('%'+ user_filter.name +'%' or
                                   User.username.like('%' + user_filter.name + '%') or
                                   User.email.like('%' + user_filter.name + '%') or
                                   User.github_url.like('%' + user_filter.name + '%') ))\
            .offset(user_filter.offset) \
            .limit(user_filter.limit)
        res = await session.execute(q)
        return res.all()
