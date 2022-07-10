from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Union


class IORMethods(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def get(self, **kwargs) -> Dict[str, Union[str, int, float, bool, Decimal]]:
        pass

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def bulk_create(self, **kwargs):
        pass

    @abstractmethod
    def update(self, by: str = "id", **kwargs):
        pass

    @abstractmethod
    def bulk_update(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, soft: bool = True, by: str = "id", **kwargs):
        pass

    @abstractmethod
    def bulk_delete(self, **kwargs):
        pass
