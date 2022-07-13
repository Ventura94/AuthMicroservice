from service_wrapper.orm.asyncio.iorm_db import IORMethods


class MongoDB(IORMethods):
    async def get(self, **kwargs):
        return await self.model.find_one(kwargs)

    async def create(self, **kwargs) -> None:
        await self.model.insert_one(kwargs)

    async def bulk_create(self, **kwargs):
        pass

    async def update(self, by: str = "id", **kwargs):
        assert by in kwargs, f"The field {by} which it is going to be updated was not defined"
        id_to_update = {by: kwargs[by]}
        if f"new_{by}" in kwargs:
            kwargs[by] = kwargs[f"new_{by}"]
            del kwargs[f"new_{by}"]
        await self.model.update_one(id_to_update, {'$set': kwargs})

    async def bulk_update(self, **kwargs):
        pass

    async def delete(self, by: str = "id", **kwargs):
        assert by in kwargs, "The field by which it is going to be deleted was not defined"
        id_to_delete = {by: kwargs[by]}
        element = await self.get(**id_to_delete)
        await element.delete()

    async def bulk_delete(self, **kwargs):
        pass
