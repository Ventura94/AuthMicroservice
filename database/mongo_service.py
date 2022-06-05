from motor import motor_asyncio


class MongoService:
    __db = None
    __collection = None

    def __init__(self, url_connection="mongodb://localhost:27017"):
        self.client = motor_asyncio.AsyncIOMotorClient(url_connection)

    @property
    def db(self):
        if self.__db is None:
            raise ValueError("Undefined database")
        return self.__db

    @db.setter
    def db(self, value):
        self.__db = self.client[value]

    @property
    def collection(self):
        if self.__collection is None:
            raise ValueError("Undefined collection")
        return self.__collection

    @collection.setter
    def collection(self, value):
        self.__collection = self.db[value]
