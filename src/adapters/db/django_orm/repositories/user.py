from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Text, Union
from src.utils.basic_logger import simple_logger as logger
from django.db.models import Q
from src.use_cases.interfaces.database import IUserDBRepository
from src.use_cases.entities.user import User as UserEntity
from src.adapters.db.django_orm.models.user import User as UserModel
from dataclasses import asdict

class UserORMRepository(IUserDBRepository):
    def __init__(self, logger: logger):
        super().__init__()
        self.logger = logger
        self.Model = UserModel
        self.ModelEntity = UserEntity

    async def remove_nulls(self, data: Dict[Text, Any]) -> Dict[Text, Any]:
        return {key: value for key, value in data.items() if value is not None}

    async def remove_invalid(self, data: Dict[Text, Any]) -> Dict[Text, Any]:
        return {key: value for key, value in data.items() if value}

    async def remove_ids(
        self, data: Dict[Text, Any], ids_list: List[Text] = None
    ) -> Dict[Text, Any]:
        if ids_list is None:
            ids_list = ["id"]
        return {key: value for key, value in data.items() if key not in ids_list}

    async def validate(self, obj: UserEntity) -> Any:
        try:
            obj = asdict(obj)
        except Exception as e:
            self.logger.error(f"Error while validating obj: {e}")
            try:
                obj = obj.__dict__
            except Exception as f:
                self.logger.error(f"Error while validating obj: {e} && {f}")
                return None
        return obj

    async def create(self, obj: UserEntity) -> Any:
        obj = await self.validate(obj)
        obj = await self.remove_nulls(obj)
        obj = await self.remove_invalid(obj)
        obj = await self.remove_ids(obj)
        try:
            return await self.MODEL.objects.acreate(**obj)
        except Exception as e:
            self.logger.error(f"Error while creating obj: {e}, with obj: {obj}")
        return None

    async def update(self) -> Any:
        pass

    async def update_filter(self, filters: Any) -> Any:
        pass

    async def delete(self, id: int) -> bool:
        pass

    async def get(self, filters: dict) -> bool:
        pass

    async def get_by_id(self, id: int) -> bool:
        pass

    async def get_by_filters(self, filters: dict) -> bool:
        pass

    async def get_all(self) -> bool:
        pass

    async def model_to_json(self, obj: Any) -> Union[None, Any, Dict[Text, Any]]:
        if obj is None:
            return None
        obj_json = obj.__dict__
        obj_json.pop("_state")
        for key, value in obj_json.items():
            if isinstance(value, datetime):
                obj_json[key] = value.strftime("%Y-%m-%d %H:%M:%S.%f")
        return obj_json

    async def model_to_dict(self, obj: Any) -> Union[None, Any, Dict[Text, Any]]:
        if obj is None:
            return None
        obj_dict = obj.__dict__
        obj_dict.pop("_state")
        return obj_dict

    async def model_to_obj(self, obj: Any) -> Union[None, Any, Dict[Text, Any]]:
        if obj is None or self.ModelEntity is None:
            return None
        obj_dict = obj.__dict__
        obj_dict.pop("_state")
        return self.ModelEntity(**obj_dict)
