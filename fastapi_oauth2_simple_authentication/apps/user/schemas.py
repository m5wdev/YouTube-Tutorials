from pydantic import BaseModel
from typing import List

from apps.blog.schemas import BlogShort


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    username: str
    email: str
    blog_posts: List[BlogShort]

    class Config:
        from_attributes = True


class UserDetails(BaseModel):
    id: int
    username: str
    email: str
    blog_posts: List[BlogShort]

    class Config:
        from_attributes = True


class UserShort(BaseModel):
    id: int
    username: str
