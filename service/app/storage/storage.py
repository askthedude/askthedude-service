from typing import Optional

from sqlalchemy.orm import Session
from .database import initialize_storage_development_mode
from .entity import User, Project, Technology, UserProjectAssociation, ProjectTechnologyAssociation
import datetime

class Storage():
    def __init__(self):
        initialize_storage_development_mode()


    def get_uset_with_id(self, id: int, session: Session) -> Optional[User]:
        return session.query(User).filter(User.id == id).first()

    def get_uset_with_email(self, email: str, session: Session) -> Optional[User]:
        return session.query(User).filter(User.email == email).first()

    def add_user_entity(self, user, session: Session) -> User:
        new_user = User(username=user.username, name=user.name,  email=user.email, github_url = user.github_url,
                        linkedin_url=user.linkedin_url, oauth=user.oauth_token)
        session.add(new_user)
        return new_user

    def add_project_entity(self, project, session: Session):
        new_user = Project(title=project.title, description=project.description, start_date=project.start_date,
                           stars=project.stars, url=project.url)
        session.add(new_user)
        return new_user

    def add_project_user_relation(self, project_id: int, user_id: int, session: Session):
        user_proj = UserProjectAssociation(project_id=project_id, user_id=user_id, create_time=datetime.datetime.now().isoformat())
        session.add(user_proj)
        return user_proj

    def add_project_technology_relation(self, project_id: int, tech_id: int, session: Session):
        proj_tech = ProjectTechnologyAssociation(project_id = project_id, technology_id = tech_id, create_time=datetime.datetime.now().isoformat())
        session.add(proj_tech)
        return proj_tech

    def add_technology(self, technology, session: Session):
        new_tech = Technology(name=technology.name, resource_url=technology.resource_url)
        session.add(new_tech)
        return new_tech
