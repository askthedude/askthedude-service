from dataclasses import dataclass
from typing import List


@dataclass
class TechnologyData:
    id: int
    name: str
    is_hot: bool
    resource_url: str


@dataclass
class PartialProjectData:
    title: str
    description: str
    stars: int
    is_active: bool
    id: int
    url: str
    start_date: str
    technologies: List[TechnologyData]
    authors: List[str]


@dataclass
class UserData:
    id: int
    username: str
    email: str
    github_url: str
    name: str
    is_active: str
    linkedin_url: str


@dataclass
class CompleteUserData:
    id: int
    username: str
    email: str
    github_url: str
    name: str
    is_active: str
    linkedin_url: str
    projects: List[PartialProjectData]


@dataclass
class StatisticsData:
    id: int
    number_of_interested: int
    subscriptions: int
    seen_frequency: int


@dataclass
class CompleteProjectData:
    title: str
    description: str
    stars: int
    is_active: bool
    id: int
    url: str
    start_date: str
    technologies: List[TechnologyData]
    users: List[UserData]
    stats: StatisticsData


@dataclass()
class ProjectSubscription:
    project_id: int
    email: str