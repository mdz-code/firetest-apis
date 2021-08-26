from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    id: str
    email: str
    hashed_password: str
    complete_name: str


class UserCreate(BaseModel):
    pass


class User(BaseModel):
    id: str
    email: str
    hashed_password: str
    complete_name: str

    class Config:
        orm_mode = True