from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from database.interfaces.user_db_actions import IUserDB
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM


class PasswordTools:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, password) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def password_verify(cls, password, password_hashed) -> bool:
        return cls.pwd_context.verify(password, password_hashed)


class UserVerify:

    @staticmethod
    async def user_authenticate(user_db: IUserDB, username: str, password: str):
        user = await user_db.get_user(username)
        if not user:
            raise ValueError("User not found")
        if not PasswordTools.password_verify(password, user.password):
            raise ValueError("Incorrect password")
        return user


class TokenTools:

    @staticmethod
    def encode_token(data: dict):
        access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data.update({"exp": access_token_expires})
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
