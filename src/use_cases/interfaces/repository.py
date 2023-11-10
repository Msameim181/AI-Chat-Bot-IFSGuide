from abc import ABC, abstractmethod
from typing import List, Any


class IRepository(ABC):
    @abstractmethod
    def validate(self, obj: Any) -> Any:
        pass

    @abstractmethod
    async def create(self, obj: Any) -> Any:
        pass

    @abstractmethod
    async def update(self, obj: Any) -> Any:
        pass

    @abstractmethod
    async def delete(self, obj_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> Any:
        pass

    @abstractmethod
    async def get_all(self) -> List[Any]:
        pass
