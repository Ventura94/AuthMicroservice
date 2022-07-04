from typing import List

from pydantic import BaseModel


class UserCredentials(BaseModel):
    username: str
    password: str


class UserInBD(BaseModel):
    username: str
    name: str
    last_name: str
    email: str
    phone: str
    password: str
    role: List[str]
    is_delete: bool
    delete_at: str


class User(BaseModel):
    username: str
    name: str
    last_name: str
    email: str
    phone: str
    role: List[str]
