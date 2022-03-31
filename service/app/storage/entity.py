from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    github_url = Column(String, nullable=False)
    linkedin_url = Column(String, nullable=False)
    oauth = Column(String)

    projects = relationship('UserProjectAssociation', back_populates='user')


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    start_date = Column(String)
    stars = Column(String)
    url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    authors = relationship('UserProjectAssociation', back_populates='project')
    technologies = relationship('ProjectTechnologyAssociation', back_populates='project')


class Technology(Base):
    __tablename__ = "technology"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    resource_url = Column(String)

    projects = relationship('ProjectTechnologyAssociation', back_populates='technology')


class UserProjectAssociation(Base):
    __tablename__ = 'user_project_association'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('project.id'))
    user_id = Column(ForeignKey('user.id'))
    create_time = Column(String)

    user = relationship('User', back_populates="projects")
    project = relationship('Project', back_populates="authors")


class ProjectTechnologyAssociation(Base):
    __tablename__ = 'project_technology_association'


    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('project.id'))
    technology_id = Column(ForeignKey('technology.id'))
    create_time = Column(String)

    technology = relationship('Technology', back_populates="projects")
    project = relationship('Project', back_populates="technologies")
