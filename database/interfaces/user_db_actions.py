from abc import ABC, abstractmethod

from pydantic import BaseModel


class IUserDB(ABC):

    @staticmethod
    @abstractmethod
    async def get_user(username: str):
        pass

    @staticmethod
    @abstractmethod
    async def register_user(user: BaseModel):
        pass

    @staticmethod
    @abstractmethod
    async def update_user(username: str, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    async def change_password(username, new_password):
        pass

    @staticmethod
    @abstractmethod
    async def delete_user(username):
        pass
