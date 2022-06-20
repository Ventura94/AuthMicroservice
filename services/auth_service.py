import re
from ServiceWrapper.services_mixins.asyncio.mixins import CreateMixin
from ServiceWrapper.orm.asyncio.mongodb import MongoDB
from database.mongo_service import MongoService
from utils.email import Email


class UserInMongo(MongoService):
    pass


class AuthService(CreateMixin):
    mongo = UserInMongo()
    mongo.db = "UserDB"
    mongo.collection = "UserCollection"

    orm_model = MongoDB(mongo.collection)

    @classmethod
    async def before_create(cls, **kwargs):
        # if not Email.is_valid(kwargs['email']):
        #    raise ValueError("This email is not correct")
        if await cls.orm_model.get(username=kwargs['username']):
            raise ValueError("This username already exist")
        if await cls.orm_model.get(email=kwargs['email']):
            raise ValueError("This email already exist")
        return kwargs
