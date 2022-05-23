from typing import Optional
import datetime

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload, contains_eager

from .entity import User, Project, Technology, UserProjectAssociation, \
    ProjectTechnologyAssociation, Role, UserRoleAssociation, UserProjectAssociationType, \
    ProjectStatistics, ProjectSubscription, UserTechnologyInterest, Comment


class Storage():
    async def healthcheck(self, session: AsyncSession):
        q = text("SELECT 1")
        res = await session.execute(q)
        return res.first()

    async def get_user_with_id(self, id: int, session: AsyncSession) -> Optional[User]:
        q = select(User) \
            .options(subqueryload(User.projects).subqueryload(UserProjectAssociation.project)) \
            .filter(User.id == id)
        res = await session.execute(q)
        return res.first()

    async def get_uset_with_email(self, email: str, username: str, session: AsyncSession) -> Optional[User]:
        q = select(User).filter(User.email == email or User.username == username)
        res = await session.execute(q)
        return res.first()

    async def get_uset_with_username(self, username: str, session: AsyncSession) -> Optional[User]:
        q = select(User).filter(User.username == username)
        res = await session.execute(q)
        return res.first()

    def add_user_entity(self, user, session: AsyncSession) -> User:
        new_user = User(username=user.username, name=user.name, hashed_password=user.password,
                        email=user.email, github_url=user.github_url,
                        linkedin_url=user.linkedin_url)
        session.add(new_user)
        return new_user

    async def update_user_entity(self, user, session: AsyncSession) -> User:
        q = select(User) \
            .filter(User.identifier_token == user.identifier_token)
        res = await session.execute(q)
        user_entity = res.first()
        user_entity.User.username=user.username
        user_entity.User.name=user.name
        user_entity.User.hashed_password = user.password
        user_entity.User.email = user.email
        user_entity.User.github_url = user.github_url
        user_entity.User.linkedin_url = user.linkedin_url
        return user_entity

    def add_project_entity(self, project, session: AsyncSession):
        new_proj = Project(title=project.title, description=project.description, start_date=project.start_date,
                           stars=project.stars, url=project.url)
        session.add(new_proj)
        return new_proj

    def add_project_user_relation(self, project_id: int, user_id: int, proj_user_rel_type_id: int,
                                  session: AsyncSession):
        user_proj = UserProjectAssociation(project_id=project_id, user_id=user_id,
                                           create_time=datetime.datetime.now().isoformat(),
                                           type_id=proj_user_rel_type_id)
        session.add(user_proj)
        return user_proj

    def add_project_technology_relation(self, project_id: int, tech_id: int, session: AsyncSession):
        proj_tech = ProjectTechnologyAssociation(project_id=project_id, technology_id=tech_id,
                                                 create_time=datetime.datetime.now().isoformat())
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
        q = select(UserProjectAssociationType.id) \
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

    async def filter_technologies(self, tech_title_filter: str, session: AsyncSession):
        q = select(Technology) \
            .filter(Technology.name.like('%' + tech_title_filter + '%'))
        res = await session.execute(q)
        return res.all()

    async def get_role_entity_with_title(self, title: str, session: AsyncSession):
        q = select(Role) \
            .filter(Role.title == title)
        res = await session.execute(q)
        return res.first()

    async def filter_projects(self, project_filter, session: AsyncSession):
        q = select(Project) \
            .join(Project.technologies).join(ProjectTechnologyAssociation.technology) \
            .join(Project.users).join(UserProjectAssociation.user).join(UserProjectAssociation.type) \
            .options(contains_eager(Project.technologies).contains_eager(ProjectTechnologyAssociation.technology)) \
            .options(contains_eager(Project.users).contains_eager(UserProjectAssociation.user)) \
            .options(contains_eager(Project.users).contains_eager(UserProjectAssociation.type)) \
            .filter(Project.title.like('%' + project_filter.title + '%')) \
            .filter(Project.description.like('%' + project_filter.description + '%')) \
            .filter(Project.is_active == project_filter.is_active) \
            .filter(UserProjectAssociationType.title == 'ADMIN') \
            .filter(
            UserProjectAssociation.user_id == project_filter.author_user_id if project_filter.author_user_id != -1 else True) \
            .distinct(Project.id) \
            .limit(project_filter.limit) \
            .offset(project_filter.offset)
        res = await session.execute(q)
        return res.unique().all()

    async def get_project_by_id(self, id: int, session: AsyncSession):
        q = select(Project) \
            .options(subqueryload(Project.technologies).subqueryload(ProjectTechnologyAssociation.technology)) \
            .options(subqueryload(Project.users).subqueryload(UserProjectAssociation.user)) \
            .options(subqueryload(Project.statistics)) \
            .options(subqueryload(Project.comments)) \
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
        q = select(User) \
            .options(subqueryload(User.projects).subqueryload(UserProjectAssociation.project)) \
            .filter(User.name.like('%' + user_filter.name + '%' or
                                   User.username.like('%' + user_filter.name + '%') or
                                   User.email.like('%' + user_filter.name + '%') or
                                   User.github_url.like('%' + user_filter.name + '%'))) \
            .offset(user_filter.offset) \
            .limit(user_filter.limit)
        res = await session.execute(q)
        return res.all()

    async def update_project_stats(self, id, stats, session: AsyncSession):
        q = select(ProjectStatistics) \
            .filter(ProjectStatistics.project_id == id)
        res = await session.execute(q)
        project_stats = res.first()
        project_stats.ProjectStatistics.seen_frequency += stats.delta_seen_frequency
        project_stats.ProjectStatistics.number_of_interested += stats.delta_number_of_interested
        project_stats.ProjectStatistics.subscriptions += stats.delta_subscriptions
        return project_stats

    def add_subscription(self,  subscription, session: AsyncSession):
        new_subscription = ProjectSubscription(project_id=subscription.project_id, email=subscription.email)
        session.add(new_subscription)
        return new_subscription

    def add_anonymous_user(self, user, session: AsyncSession):
        user = User(identifier_token=user.identifier_token, anonymous=True)
        session.add(user)
        return user

    async def get_user_with_identifier_token(self, identifier_token, session: AsyncSession):
        q = select(User)\
                .filter(User.identifier_token == identifier_token)
        res = await session.execute(q)
        return res.first()

    def add_user_technology_interest(self, user_technology, session: AsyncSession):
        user_tech = UserTechnologyInterest(user_id=user_technology.user_id, technology_id=user_technology.technology_id)
        session.add(user_tech)
        return user_tech

    def add_comment_to_project(self, comment, session: AsyncSession):
        comment = Comment(project_id=comment.project_id, user_id = comment.user_id, parent_comment_id=comment.parent_comment_id
                          , content=comment.content, created_timestamp=datetime.datetime.now().isoformat(), edited_timestamp=datetime.datetime.now().isoformat(),
                          active=True)
        session.add(comment)
        return comment
# export singleton storage
storage = Storage()
