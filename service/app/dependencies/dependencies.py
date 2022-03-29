# put here global project dependencies for indirection level between components
from typing import Optional
from storage.storage import Storage
from pydantic import BaseModel
from typing import List


storage = Storage()


class GetUser(BaseModel):
    id: int
    name: str
    username: str
    email: str
    is_active: bool
    github_url: str
    linkedin_url: str


class PostUser(BaseModel):
    name: str
    username: str
    email: str
    github_url: str
    linkedin_url: Optional[str]
    oauth_token: str


class PostProject(BaseModel):
    title: str
    description: str
    start_date: str
    stars: str
    github_url: str
    url: str
    user_ids: List[int]
    technology_ids: List[int]


class GetProject(BaseModel):
    title: str
    description: str
    start_date: str
    stars: str
    github_url: str
    url: str
    user_ids: List[int]
    technology_ids: List[int]


class PostTechnology(BaseModel):
    name: str
    resource_url: str


class GetTechnology(BaseModel):
    id: int
    name: str
    resource_url: str