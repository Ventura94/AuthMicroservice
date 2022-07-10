from typing import Dict

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from passlib.context import CryptContext
from service_wrapper.orm.asyncio.mongodb import MongoDB
from service_wrapper.services.asyncio.service import CreateMixin, DeleteMixin, UpdateMixin
from starlette import status

from database.mongo_service import MongoService
from schemas.user import UserInBD, User
from settings import SECRET_KEY, ALGORITHM
from utils.email import Email


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
        except JWTClaimsError:
            raise self.authorized_exception("If any claim is invalid in any way.")
        except ExpiredSignatureError:
            raise self.authorized_exception("If the signature has expired.")
        except JWTError:
            raise self.authorized_exception("If the signature is invalid in any way.")
        user = await self.orm_model.get(username=payload['username'])
        if not user or user.get("is_delete", False):
            raise self.authorized_exception("User don't exist")
        return User(**user)

    async def before_create(self, **kwargs) -> Dict[str, str]:
        if not Email.is_valid(kwargs["email"]):
            raise self.authorized_exception("This email is not correct")
        if await self.orm_model.get(username=kwargs["username"]):
            raise self.authorized_exception("This username already exist")
        if await self.orm_model.get(email=kwargs["email"]):
            raise self.authorized_exception("This email already exist")
        kwargs["password"] = self.pwd_context.hash(kwargs["password"])
        return kwargs

    async def user_authenticate(self, username: str, password: str) -> User:
        if Email.is_email(username):
            user = await self.orm_model.get(email=username)
        else:
            user = await self.orm_model.get(username=username)
        user = UserInBD(**user)
        if not user or user.is_delete:
            raise self.authorized_exception("User not found")
        if not self.pwd_context.verify(password, user.password):
            raise self.authorized_exception("Incorrect password")
        return User(**user.dict())
