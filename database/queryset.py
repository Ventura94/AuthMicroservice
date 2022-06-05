from settings import auth_database
from schemas.user import UserInBD, User
from database.interfaces.user_db_actions import IUserDB


class UserMongoDB(IUserDB):
    auth_database.db = "UserDB"
    auth_database.collection = "UserCollection"

    @staticmethod
    async def get_user(username: str) -> UserInBD:
        user_data = await auth_database.collection.find_one({
            "$or": [
                {"username": username},
                {"email": username}]
        })
        if not user_data:
            raise ValueError("User Not Exist")
        return UserInBD(**user_data)

    @staticmethod
    async def register_user(user: UserInBD) -> User:
        user_data = await auth_database.collection.find_one({
            "$or": [
                {"username": user.username},
                {"email": user.email}]
        })
        if user_data:
            raise ValueError("Username or Email exist")
        result = await auth_database.collection.insert_one(user.dict())
        return User(**result)

    async def update_user(self):
        pass

    async def delete_user(self):
        pass

    async def change_password(self):
        pass
