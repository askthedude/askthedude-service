from dataclasses import dataclass
from typing import List


@dataclass
class TechnologyDeclaration:
    id: int
    title: str
    is_hot: bool
    resource_url: str


@dataclass
class ProjectDeclaration:
    title: str
    description: str
    stars: int
    is_active: bool
    id: int
    url: str
    start_date: str
    technologies: List[TechnologyDeclaration]

