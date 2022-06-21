from ServiceWrapper.orm.asyncio.mongodb import MongoDB
from ServiceWrapper.services_mixins.asyncio.mixins import CreateMixin
from passlib.context import CryptContext

from database.mongo_service import MongoService
from schemas.user import UserInBD
from utils.email import Email


class UserInMongo:
    mongo = MongoService()
    mongo.db = "UserDB"
    mongo.collection = "UserCollection"


class AuthService(CreateMixin):
    orm_model = MongoDB(UserInMongo.mongo.collection)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def before_create(self, **kwargs):
        if not Email.is_valid(kwargs['email']):
            raise ValueError("This email is not correct")
        if await self.orm_model.get(username=kwargs['username']):
            raise ValueError("This username already exist")
        if await self.orm_model.get(email=kwargs['email']):
            raise ValueError("This email already exist")
        kwargs["password"] = self.pwd_context.hash(kwargs["password"])
        return kwargs

    async def user_authenticate(self, username: str, password: str):
        if Email.is_email(username):
            user = await self.orm_model.get(email=username)
        else:
            user = await self.orm_model.get(username=username)
        if not user:
            raise ValueError("User not found")
        user = UserInBD(**user)
        if not self.pwd_context.verify(password, user.password):
            raise ValueError("Incorrect password")
        return user
