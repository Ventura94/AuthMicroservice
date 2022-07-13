from typing import List

from pydantic import BaseModel, Field


class UserCredentials(BaseModel):
    username: str
    password: str


class UserInBD(BaseModel):
    user_id: str
    username: str
    name: str
    last_name: str
    email: str
    phone: str
    password: str
    role: List[str]
    is_delete: bool
    delete_at: str = Field(default=None)


class User(BaseModel):
    username: str
    name: str
    last_name: str
    email: str
    phone: str
    role: List[str]


class UserO2Auth(BaseModel):
    user_id: str
    username: str
    name: str
    last_name: str
    email: str
    phone: str
    role: List[str]
