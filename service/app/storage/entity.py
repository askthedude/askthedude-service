from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    github_url = Column(String)
    linkedin_url = Column(String)
    oauth = Column(String, nullable=True)
    identifier_token = Column(String, nullable=True, unique=True)
    anonymous = Column(Boolean, nullable=True, default=False)

    projects = relationship('UserProjectAssociation', back_populates='user')
    roles = relationship('UserRoleAssociation', back_populates="user")


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    start_date = Column(String)
    stars = Column(String)
    url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    users = relationship('UserProjectAssociation', back_populates='project')
    technologies = relationship('ProjectTechnologyAssociation', back_populates='project')
    statistics = relationship('ProjectStatistics', back_populates="project")


class Technology(Base):
    __tablename__ = "technology"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    resource_url = Column(String)
    is_hot = Column(Boolean, default=False)

    projects = relationship('ProjectTechnologyAssociation', back_populates='technology')


class UserProjectAssociation(Base):
    __tablename__ = 'user_project_association'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('project.id'), nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    create_time = Column(String)
    is_active = Column(Boolean, default=True)
    type_id = Column(ForeignKey('user_project_association_type.id'), nullable=False)

    user = relationship('User', back_populates="projects")
    project = relationship('Project', back_populates="users")
    type = relationship("UserProjectAssociationType")


class UserProjectAssociationType(Base):
    __tablename__ = 'user_project_association_type'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)


class ProjectTechnologyAssociation(Base):
    __tablename__ = 'project_technology_association'


    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('project.id'), nullable=False)
    technology_id = Column(ForeignKey('technology.id'), nullable=False)
    create_time = Column(String)

    technology = relationship('Technology', back_populates="projects")
    project = relationship('Project', back_populates="technologies")


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    users = relationship('UserRoleAssociation', back_populates="role")


class UserRoleAssociation(Base):
    __tablename__ = 'user_role_association'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    role_id = Column(ForeignKey('role.id'), nullable=False)

    user = relationship('User', back_populates="roles")
    role = relationship('Role', back_populates="users")


class ProjectStatistics(Base):
    __tablename__ = 'project_statistics'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('project.id'), nullable=False)
    seen_frequency = Column(Integer, default=0)
    number_of_interested = Column(Integer, default=0)
    subscriptions = Column(Integer, default=0)

    project = relationship('Project', back_populates="statistics")


class ProjectSubscription(Base):
    __tablename__ = 'project_subscription'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('project.id'), nullable=False)
    active = Column(Boolean, default=True)
    email = Column(String, nullable=False)


class UserTechnologyInterest(Base):
    __tablename__ = 'user_technology_interest'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    technology_id = Column(ForeignKey('technology.id'), nullable=False)
    active = Column(Boolean, default=True)