from abc import ABC, abstractmethod
from typing import List, Any
from datetime import timedelta


class IDBRepository(ABC):
    @abstractmethod
    def validate(obj: Any) -> Any:
        pass

    @abstractmethod
    async def create(obj: Any) -> Any:
        pass

    @abstractmethod
    async def update(obj: Any) -> Any:
        pass

    @abstractmethod
    async def delete(obj_id: int) -> bool:
        pass

    @abstractmethod
    async def get(filters: dict) -> Any:
        pass

    @abstractmethod
    async def get_by_id(obj_id: int) -> Any:
        pass

    @abstractmethod
    async def get_all() -> List[Any]:
        pass

    @abstractmethod
    async def get_by_status(status: str) -> List[Any]:
        pass

    @abstractmethod
    async def get_by_filters(filters: dict) -> Any:
        pass

    @abstractmethod
    async def update_filter(filters: dict, obj: Any) -> Any:
        pass

    @abstractmethod
    async def get_potential_objs(window_frame: timedelta) -> List[Any]:
        pass

    async def model_to_json(self, obj: Any) -> Any:
        pass

    async def model_to_dict(self, obj: Any) -> Any:
        pass

    async def model_to_obj(self, obj: Any) -> Any:
        return