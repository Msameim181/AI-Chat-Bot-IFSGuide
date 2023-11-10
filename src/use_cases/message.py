from src.use_cases.interfaces.database import IMessageDBRepository
from src.use_cases.interaction import InteractionUseCase
from src.use_cases.exceptions import UserNotAuthorized, InteractionNotFound
import asyncio
from src.utils.basic_logger import simple_logger as logger
from src.entities.message import Message
from typing import Union


class MessageUseCase:
    def __init__(
        self,
        database_repository: IMessageDBRepository,
        interaction_use_case: InteractionUseCase,
        logger: logger,
    ):
        self.database_repository = database_repository
        self.interaction_use_case = interaction_use_case
        self.logger = logger

    async def execute(self, **kwargs) -> None:
        pass

    def sync_execute(self, **kwargs) -> None:
        asyncio.run(self.execute_job(**kwargs))

    async def add_new_message(self, message: Message, user_id: str) -> Union[Message, None]:
        interaction = await self.interaction_use_case.get_interaction_by_id(message.interaction_id)
        if interaction is None or not interaction:
            raise InteractionNotFound("Interaction not found with provided information")
        if interaction.user_id != user_id:
            raise UserNotAuthorized("User not authorized to access this interaction")
        response = await self.database_repository.create(message)
        if response is None or not response:
            return None
        return await self.database_repository.model_to_obj(response)

    async def get_message_by_id(self, id: str) -> Message:
        message = await self.database_repository.get_by_id(id)
        if message is None or not message:
            return None
        return await self.database_repository.model_to_obj(message)

    async def get_all_messages(self) -> list[Message]:
        messages = await self.database_repository.get_all()
        if messages is None or not messages:
            return None
        return [await self.database_repository.model_to_obj(message) for message in messages]

    async def get_messages_by_interaction_id(self, interaction_id: str) -> Message:
        messages = await self.database_repository.get_all_by_filters({"interaction_id": interaction_id})
        if messages is None or not messages:
            return None
        return [
            await self.database_repository.model_to_obj(message)
            for message in messages
        ]
    
    async def get_messages_by_interaction_id_json(self, interaction_id: str) -> Message:
        messages = await self.database_repository.get_all_by_filters({"interaction_id": interaction_id})
        if messages is None or not messages:
            return None
        return [
            await self.database_repository.model_to_json(message)
            for message in messages
        ]

    async def update_message(self, message: Message) -> Union[Message, None]:
        response = await self.database_repository.update_filter({"id": message.id}, message)
        if response is None or not response:
            return None
        return await self.database_repository.model_to_obj(response)

    async def delete_message(self, id: str) -> bool:
        response = await self.database_repository.delete(id)
        return bool(
            response is not None and (not isinstance(response, tuple) or response[0])
        )

    async def retrieve_all(self, interaction_id: str, user_id: str) -> list:
        interaction = await self.interaction_use_case.get_interaction_by_id(interaction_id)
        if interaction is None or not interaction:
            raise InteractionNotFound("Interaction and Messages not found with provided information")
        if interaction.user_id != user_id:
            raise UserNotAuthorized("User not authorized to access this interaction")
        return await self.get_messages_by_interaction_id_json(interaction_id)