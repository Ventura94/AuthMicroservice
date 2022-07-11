from abc import ABC

from service_wrapper.interfaces.iservice import IService


class CreateMixin(IService, ABC):
    async def create(self, **kwargs) -> None:
        data = await self.before_create(**kwargs)
        await self.orm_model.create(**data)
        await self.after_created(**data)

    async def bulk_create(self, **kwargs) -> None:
        data = await self.before_bulk_create(**kwargs)
        await self.orm_model.bulk_create(**data)
        await self.after_bulk_created(**data)

    async def before_create(self, **kwargs):
        return kwargs

    async def after_created(self, **kwargs):
        pass

    async def before_bulk_create(self, **kwargs):
        return kwargs

    async def after_bulk_created(self, **kwargs):
        pass


class UpdateMixin(IService, ABC):

    async def update(self, by: str = "id", **kwargs):
        assert by in kwargs.keys(), "The field by which it is going to be updated was not defined"
        data = await self.before_update(**kwargs)
        await self.orm_model.update(by, **data)
        await self.after_update(**data)

    async def bulk_update(self, partial: bool = False, **kwargs):
        pass

    async def before_update(self, **kwargs):
        return kwargs

    async def after_update(self, **kwargs):
        pass

    async def before_bulk_update(self, **kwargs):
        return kwargs

    async def after_bulk_update(self, **kwargs):
        pass


class DeleteMixin(IService, ABC):
    async def delete(self, soft: bool = True, by: str = "id", **kwargs):
        assert by in kwargs.keys(), f"The field {by} which it is going to be updated was not defined"
        data = await self.before_delete(**kwargs)
        if soft:
            data.update({"is_delete": True})
            await self.orm_model.update(by=by, **data)
        else:
            await self.orm_model.delete(by=by, **data)
        await self.after_delete(**data)

    async def bulk_delete(self, soft: bool = True, **kwargs):
        data = await self.before_delete(**kwargs)
        if soft:
            await self.orm_model.bulk_update(**data)
        else:
            await self.orm_model.bulk_delete(**data)
        await self.after_delete(**data)

    async def before_delete(self, **kwargs):
        return kwargs

    async def after_delete(self, **kwargs):
        pass

    async def before_bulk_delete(self, **kwargs):
        return kwargs

    async def after_bulk_delete(self, **kwargs):
        pass
