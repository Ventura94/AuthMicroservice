from typing import Dict

from ServiceWrapper.orm.asyncio.mongodb import MongoDB
from ServiceWrapper.services.asyncio.service import Create
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from passlib.context import CryptContext
from starlette import status

from database.mongo_service import MongoService
from schemas.user import UserInBD, User
from settings import SECRET_KEY, ALGORITHM
from utils.email import Email


class UserInMongo:
    mongo = MongoService()
    mongo.db = "UserDB"
    mongo.collection = "UserCollection"


class AuthService(Create):
    orm_model = MongoDB(UserInMongo.mongo.collection)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", description="authorization")

    async def o2auth(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM, ])
            user = User(**payload)
        except [JWTError, ExpiredSignatureError, JWTClaimsError]:
            raise credentials_exception
        user = await self.orm_model.get(username=user.username)
        if not user or not user.get("is_active", None):
            raise credentials_exception
        return user

    async def before_create(self, **kwargs) -> Dict[str, str]:
        if not Email.is_valid(kwargs["email"]):
            raise ValueError("This email is not correct")
        if await self.orm_model.get(username=kwargs["username"]):
            raise ValueError("This username already exist")
        if await self.orm_model.get(email=kwargs["email"]):
            raise ValueError("This email already exist")
        kwargs["password"] = self.pwd_context.hash(kwargs["password"])
        return kwargs

    async def user_authenticate(self, username: str, password: str) -> User:
        if Email.is_email(username):
            user = await self.orm_model.get(email=username)
        else:
            user = await self.orm_model.get(username=username)
        user = UserInBD(**user)
        if not user or not user.is_active:
            raise ValueError("User not found")
        if not self.pwd_context.verify(password, user.password):
            raise ValueError("Incorrect password")
        return User(**user.dict())
