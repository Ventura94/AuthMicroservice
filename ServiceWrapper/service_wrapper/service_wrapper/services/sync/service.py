from abc import ABC

from service_wrapper.interfaces.iservice import IService


class CreateMixin(IService, ABC):
    def create(self, **kwargs) -> None:
        data = self.before_create(**kwargs)
        self.orm_model.create(**data)
        self.after_created(**data)

    def bulk_create(self, **kwargs) -> None:
        data = self.before_bulk_create(**kwargs)
        self.orm_model.bulk_create(**data)
        self.after_created(**data)

    def before_create(self, **kwargs):
        return kwargs

    def after_created(self, **kwargs):
        pass

    def before_bulk_create(self, **kwargs):
        return kwargs


class UpdateMixin(IService):
    def update(self, partial: bool = False, **kwargs):
        pass

    def bulk_update(self, partial: bool = False, **kwargs):
        pass

    def before_update(self, **kwargs):
        return kwargs

    def after_update(self, **kwargs):
        pass

    def before_bulk_update(self, **kwargs):
        return kwargs

    def after_bulk_update(self, **kwargs):
        pass


class DeleteMixin(IService):
    def delete(self, soft: bool = True, **kwargs):
        data = self.before_delete(**kwargs)
        if soft:
            data.update({"is_delete": True})
            self.orm_model.update(**data)
        else:
            self.orm_model.delete(**data)
        self.after_delete(**data)

    def bulk_delete(self, soft: bool = True, **kwargs):
        data = self.before_delete(**kwargs)
        if soft:
            data.update({"rife": {"is_delete": True}})
            self.orm_model.bulk_update(**data)
        else:
            self.orm_model.bulk_delete(**data)
        self.after_delete(**data)

    def before_delete(self, **kwargs):
        return kwargs

    def after_delete(self, **kwargs):
        pass

    def before_bulk_delete(self, **kwargs):
        return kwargs

    def after_bulk_delete(self, **kwargs):
        pass
