from src.use_cases.interfaces.database import IMessageDBRepository
from src.use_cases.interaction import InteractionUseCase
from src.use_cases.ai_service import AIServiceUseCase
from src.use_cases.exceptions import UserNotAuthorized, InteractionNotFound
import asyncio
from src.utils.basic_logger import simple_logger as logger
from src.entities.message import Message, RoleType
from typing import Union, List


class MessageUseCase:
    def __init__(
        self,
        database_repository: IMessageDBRepository,
        interaction_use_case: InteractionUseCase,
        ai_service_use_case: AIServiceUseCase,
        logger: logger,
    ):
        self.database_repository = database_repository
        self.interaction_use_case = interaction_use_case
        self.ai_service_use_case = ai_service_use_case
        self.logger = logger

    async def execute(self, messages, interaction_id: str, user_id: str) -> None:
        if self.ai_service_use_case is None:
            raise Exception("AI Service not initialized")
        try:
            response = await self.ai_service_use_case.execute(messages=messages)
            response = await self.add_new_message(
                Message(
                    id=None,
                    interaction_id=interaction_id,
                    role=RoleType.AI.value,
                    content=response,
                ),
                user_id=user_id,
            )
            return response
        except Exception as e:
            raise e

    def sync_execute(self, **kwargs) -> None:
        asyncio.run(self.execute_job(**kwargs))

    async def prepare_messages(self, messages: List[Message]) -> Message:
        return [
            {"role": message.role, "content": message.content} for message in messages
        ]

    async def add_new_message(
        self, message: Message, user_id: str, will_ai_respond: bool = False
    ) -> Union[Message, None]:
        interaction = await self.interaction_use_case.get_interaction_by_id(
            message.interaction_id
        )
        if interaction is None or not interaction:
            raise InteractionNotFound("Interaction not found with provided information")
        if interaction.user_id != user_id:
            raise UserNotAuthorized("User not authorized to access this interaction")
        response = await self.database_repository.create(message)
        if response is None or not response:
            return None
        if will_ai_respond:
            previous_messages = await self.get_messages_by_interaction_id(
                message.interaction_id
            )
            previous_messages = await self.prepare_messages(previous_messages)
            response = await self.execute(
                messages=previous_messages,
                interaction_id=interaction.id,
                user_id=interaction.user_id,
            )
        return await self.database_repository.model_to_obj(response)

    async def get_message_by_id(self, id: str) -> Message:
        message = await self.database_repository.get_by_id(id)
        if message is None or not message:
            return None
        return await self.database_repository.model_to_obj(message)

    async def get_all_messages(self) -> List[Message]:
        messages = await self.database_repository.get_all()
        if messages is None or not messages:
            return None
        return [
            await self.database_repository.model_to_obj(message) for message in messages
        ]

    async def get_messages_by_interaction_id(self, interaction_id: str) -> Message:
        messages = await self.database_repository.get_all_by_filters(
            {"interaction_id": interaction_id}
        )
        if messages is None or not messages:
            return None
        return [
            await self.database_repository.model_to_obj(message) for message in messages
        ]

    async def get_messages_by_interaction_id_json(self, interaction_id: str) -> Message:
        messages = await self.database_repository.get_all_by_filters(
            {"interaction_id": interaction_id}
        )
        if messages is None or not messages:
            return None
        return [
            await self.database_repository.model_to_json(message)
            for message in messages
        ]

    async def update_message(self, message: Message) -> Union[Message, None]:
        response = await self.database_repository.update_filter(
            {"id": message.id}, message
        )
        if response is None or not response:
            return None
        return await self.database_repository.model_to_obj(response)

    async def delete_message(self, id: str) -> bool:
        response = await self.database_repository.delete(id)
        return bool(
            response is not None and (not isinstance(response, tuple) or response[0])
        )

    async def retrieve_all(self, interaction_id: str, user_id: str) -> list:
        interaction = await self.interaction_use_case.get_interaction_by_id(
            interaction_id
        )
        if interaction is None or not interaction:
            raise InteractionNotFound(
                "Interaction and Messages not found with provided information"
            )
        if interaction.user_id != user_id:
            raise UserNotAuthorized("User not authorized to access this interaction")
        return await self.get_messages_by_interaction_id_json(interaction_id)
