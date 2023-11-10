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
    async def update_filter(filters: dict, obj: Any) -> Any:
        pass

    @abstractmethod
    async def get(filters: dict, **kwarg) -> Any:
        pass

    @abstractmethod
    async def get_by_id(obj_id: int, **kwarg) -> Any:
        pass

    @abstractmethod
    async def get_all(**kwarg) -> List[Any]:
        pass

    @abstractmethod
    async def get_all_by_filters(filters: dict, **kwarg) -> Any:
        pass

    @abstractmethod
    async def delete(obj_id: int) -> bool:
        pass

    @abstractmethod
    async def model_to_json(obj: Any) -> Any:
        pass

    @abstractmethod
    async def model_to_dict(obj: Any) -> Any:
        pass

    @abstractmethod
    async def model_to_obj(obj: Any) -> Any:
        pass


class IUserDBRepository(IDBRepository):
    pass
class IInteractionDBRepository(IDBRepository):
    pass
class IMessageDBRepository(IDBRepository):
    pass
