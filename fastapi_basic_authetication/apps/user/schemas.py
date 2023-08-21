from pydantic import BaseModel


# class UserBase(BaseModel):
#     email: str


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserDelete(BaseModel):
    username: str
    password: str
