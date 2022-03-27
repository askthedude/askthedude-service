from fastapi import APIRouter
from pydantic import BaseModel
from dataclasses import dataclass


router = APIRouter()


@dataclass
class GetUser(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    is_active: bool


@dataclass
class PostUser(BaseModel):
    name: str
    surname: str
    email: str
    password: str


@router.get("/user/{id}", response_model=GetUser, )
async def get_user(id: str):
    return GetUser(1, 'nika', 'sakana', 'email.com', True)


@router.post("/user/", response_model=GetUser)
async def add_user(user: PostUser):
    return GetUser(1, 'nika', 'sakana', 'email.com', True)