from src.use_cases.interfaces.database import IInteractionDBRepository
from src.use_cases.interfaces.database import IMessageDBRepository
import asyncio
from src.utils.basic_logger import simple_logger as logger
from src.entities.interaction import Interaction
from typing import Union, List


class InteractionUseCase:
    def __init__(
        self,
        database_repository: IInteractionDBRepository,
        message_database_repository: IMessageDBRepository,
        logger: logger,
    ):
        self.database_repository = database_repository
        self.message_database_repository = message_database_repository
        self.logger = logger

    async def execute(self, **kwargs) -> None:
        pass

    def sync_execute(self, **kwargs) -> None:
        asyncio.run(self.execute_job(**kwargs))

    async def add_new_interaction(
        self, interaction: Interaction
    ) -> Union[Interaction, None]:
        response = await self.database_repository.create(interaction)
        if response is None or not response:
            return None
        return await self.database_repository.model_to_obj(response)

    async def get_interaction_by_id(self, id: str) -> Interaction:
        interaction = await self.database_repository.get_by_id(id)
        if interaction is None or not interaction:
            return None
        return await self.database_repository.model_to_obj(interaction)

    async def get_all_interactions(self) -> List[Interaction]:
        interactions = await self.database_repository.get_all()
        if interactions is None or not interactions:
            return None
        return [
            await self.database_repository.model_to_obj(interaction)
            for interaction in interactions
        ]

    async def get_interaction_by_user_id(self, user_id: str) -> Interaction:
        interaction = await self.database_repository.get({"user_id": user_id})
        if interaction is None or not interaction:
            return None
        return await self.database_repository.model_to_obj(interaction)

    async def get_all_interaction_by_user_id(self, user_id: str) -> Interaction:
        interaction = await self.database_repository.get_all_by_filters(
            {"user_id": user_id}
        )
        if interaction is None or not interaction:
            return None
        return [
            await self.database_repository.model_to_obj(interaction)
            for interaction in interaction
        ]

    async def update_interaction(
        self, interaction: Interaction
    ) -> Union[Interaction, None]:
        response = await self.database_repository.update_filter(
            {"id": interaction.id}, interaction
        )
        if response is None or not response:
            return None
        return await self.database_repository.model_to_obj(response)

    async def delete_interaction(self, id: str) -> bool:
        response = await self.database_repository.delete(id)
        return bool(
            response is not None and (not isinstance(response, tuple) or response[0])
        )

    async def retrieve_all(self, user_id: str) -> list:
        interactions = await self.database_repository.get_all_by_filters(
            {"user_id": user_id}
        )
        if interactions is None or not interactions:
            return None
        responses = []
        for interaction in interactions:
            messages = interaction.messages.all()
            temp_interaction = await self.database_repository.model_to_json(interaction)
            temp_interaction["messages"] = []
            for message in messages:
                temp_message = await self.message_database_repository.model_to_json(
                    message
                )
                temp_interaction["messages"].append(temp_message)
            responses.append(temp_interaction)
        return responses
