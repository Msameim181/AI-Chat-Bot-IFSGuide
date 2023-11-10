from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Text, Union
from src.utils.basic_logger import simple_logger as logger
from django.db.models import Q
from src.use_cases.interfaces.database import IMessageDBRepository
from src.entities.message import Message as MessageEntity
from src.adapters.db.django_orm.core.models.message import Message as MessageModel
from dataclasses import asdict

class MessageDBRepository(IMessageDBRepository):
    def __init__(self, logger: logger):
        super().__init__()
        self.logger = logger
        self.MODEL = MessageModel
        self.MODEL_ENTITY = MessageEntity

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

    async def validate(self, obj: MessageEntity) -> Any:
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

    async def create(self, obj: MessageEntity) -> Any:
        obj = await self.validate(obj)
        obj = await self.remove_nulls(obj)
        obj = await self.remove_invalid(obj)
        obj = await self.remove_ids(obj)
        try:
            return await self.MODEL.objects.acreate(**obj)
        except Exception as e:
            self.logger.error(f"Error while creating obj: {e}, with obj: {obj}")
        return None

    async def update(self, obj: MessageModel) -> Any:
        if not isinstance(obj, MessageModel):
            return None
        try:
            await obj.asave()
            await obj.arefresh_from_db()
            return obj
        except Exception as e:
            self.logger.error(f"Error while updating obj: {e}, with obj: {obj}")
        return None

    async def update_filter(self, filters: dict, obj: MessageEntity) -> Any:
        obj = await self.validate(obj)
        obj = await self.remove_nulls(obj)
        obj = await self.remove_ids(obj)
        try:
            await self.MODEL.objects.filter(**filters).aupdate(**obj)
            return await self.MODEL.objects.filter(**filters).afirst()
        except Exception as e:
            self.logger.error(
                f"Error while updating obj with filters: {filters}; with obj: {obj}; error: {e}"
            )
        return None

    async def delete(self, obj_id: int) -> bool:
        try:
            return await self.MODEL.objects.filter(id=obj_id).adelete()
        except Exception as e:
            self.logger.error(f"Error while deleting obj with id: {obj_id}; error: {e}")
            return False

    async def get(self, filters: dict) -> MessageModel:
        return await self.MODEL.objects.filter(**filters).afirst()

    async def get_by_id(self, obj_id: int) -> MessageModel:
        return await self.MODEL.objects.filter(id=obj_id).afirst()

    async def get_all(self) -> list:
        return self.MODEL.objects.all()

    async def get_all_by_filters(self, filters: dict) -> list:
        return self.MODEL.objects.filter(**filters).all()

    async def model_to_json(self, obj: Any) -> Union[None, Any, Dict[Text, Any]]:
        if obj is None:
            return None
        obj_json = obj.__dict__.copy()
        obj_json.pop("_state", None)
        obj_json.pop("_prefetched_objects_cache", None)
        obj_json.pop("interaction_id", None)
        for key, value in obj_json.items():
            if isinstance(value, datetime):
                obj_json[key] = value.strftime("%Y-%m-%d %H:%M:%S.%f")
        return obj_json

    async def model_to_dict(self, obj: Any) -> Union[None, Any, Dict[Text, Any]]:
        if obj is None:
            return None
        obj_dict = obj.__dict__.copy()
        obj_dict.pop("_state", None)
        obj_dict.pop("_prefetched_objects_cache", None)
        return obj_dict

    async def model_to_obj(self, obj: Any) -> Union[None, Any, Dict[Text, Any]]:
        if obj is None or self.MODEL_ENTITY is None:
            return None
        obj_dict = obj.__dict__.copy()
        obj_dict.pop("_state", None)
        obj_dict.pop("_prefetched_objects_cache", None)
        return self.MODEL_ENTITY(**obj_dict)
