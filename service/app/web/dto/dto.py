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
    password: str
    email: str
    github_url: Optional[str]
    linkedin_url: Optional[str]

class SignInUser(BaseModel):
    username: str
    password: str


class PostProject(BaseModel):
    title: str
    description: str
    start_date: str
    stars: str
    github_url: str
    url: str
    user_id: int
    technology_ids: List[int]


class GetProject(BaseModel):
    title: str
    description: str
    start_date: str
    stars: str
    github_url: str
    url: str
    user_id: int
    technology_ids: List[int]


class PostTechnology(BaseModel):
    name: str
    resource_url: str


class GetTechnology(BaseModel):
    id: int
    name: str
    resource_url: str


LIMIT_CONSTANT = 10
OFFSET_INIT_CONSTANT = 0


# Below Dto is filled with default values to have flags for cases when outputs
# shouldn't be filtered by specific field
class ProjectFilter(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    start_date: Optional[str]
    stars: Optional[int] = -1
    is_active: Optional[bool] = True
    author_user_id: Optional[int] = -1
    technology_ids: Optional[List[int]]=[]
    # below is paging functionality
    offset: Optional[int] = OFFSET_INIT_CONSTANT
    limit: Optional[int] = LIMIT_CONSTANT


class UserFilter(BaseModel):
    name: Optional[str] = ""
    offset: Optional[int] = OFFSET_INIT_CONSTANT
    limit: Optional[int] = LIMIT_CONSTANT


class PostRole(BaseModel):
    id: Optional[int]
    title: str


class GetRole(BaseModel):
    id: int
    title: str


class PostStatistics(BaseModel):
    delta_seen_frequency: Optional[int] = 0
    delta_number_of_interested: Optional[int] = 0
    delta_subscriptions: Optional[int] = 0

