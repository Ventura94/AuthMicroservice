from typing import Dict

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from passlib.context import CryptContext
from starlette import status

from database.mongo_service import MongoService
from schemas.user import UserInBD, UserO2Auth
from service_wrapper.orm.asyncio.mongodb import MongoDB
from service_wrapper.services.asyncio.service import CreateMixin, DeleteMixin, UpdateMixin
from settings import SECRET_KEY, ALGORITHM
from tools.email import Email


class UserInMongo:
    mongo = MongoService()
    mongo.db = "UserDB"
    mongo.collection = "UserCollection"


class AuthService(CreateMixin, UpdateMixin, DeleteMixin):
    orm_model = MongoDB(UserInMongo.mongo.collection)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", description="authorization")

    @staticmethod
    def authorized_exception(message: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )

    async def o2auth(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM, ])
        except JWTClaimsError as jwtce:
            raise self.authorized_exception("If any claim is invalid in any way.") from jwtce
        except ExpiredSignatureError as ese:
            raise self.authorized_exception("If the signature has expired.") from ese
        except JWTError as jwte:
            raise self.authorized_exception("If the signature is invalid in any way.") from jwte
        user = await self.orm_model.get(user_id=payload['user_id'])
        if not user or user.get("is_delete", False):
            raise self.authorized_exception("User don't exist")
        return UserO2Auth(**user)

    async def before_create(self, **kwargs) -> Dict[str, str]:
        if not Email.is_valid(kwargs["email"]):
            raise self.authorized_exception("This email is not correct")
        await self.uniques_verify(**kwargs)
        kwargs["password"] = self.pwd_context.hash(kwargs["password"])
        return kwargs

    async def user_authenticate(self, username: str, password: str) -> UserO2Auth:
        if Email.is_email(username):
            user = await self.orm_model.get(email=username)
        else:
            user = await self.orm_model.get(username=username)
        if not user or user.get("is_delete", False):
            raise self.authorized_exception("User not found")
        user = UserInBD(**user)
        if not self.pwd_context.verify(password, user.password):
            raise self.authorized_exception("Incorrect password")
        return UserO2Auth(**user.dict())

    async def before_update(self, **kwargs):
        if kwargs.get("password"):
            kwargs["password"] = self.pwd_context.hash(kwargs["password"])
        await self.uniques_verify(**kwargs)
        return kwargs

    async def uniques_verify(self, **kwargs) -> None:
        if kwargs.get("username") and await self.is_exist_in_db(username=kwargs["username"]):
            raise self.authorized_exception("This username already exist")
        if kwargs.get("email") and await self.is_exist_in_db(email=kwargs["email"]):
            raise self.authorized_exception("This email already exist")

    async def is_exist_in_db(self, **kwargs) -> bool:
        db_result = await self.orm_model.get(**kwargs)
        if db_result:
            return True
        return False
