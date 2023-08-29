from pydantic import BaseModel


class BlogCreate(BaseModel):
    title: str
    description: str
    published: bool
    author_id: int


class Blog(BlogCreate):
    id: int


class BlogShort(BaseModel):
    id: int
    title: str


class User(BaseModel):
    id: int
    username: str


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    password: str


class BlogDetail(BaseModel):
    id: int
    title: str
    description: str
    published: bool
    author: User
