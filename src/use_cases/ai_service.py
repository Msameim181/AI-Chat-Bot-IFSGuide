from src.use_cases.interfaces.database import IMessageDBRepository
import asyncio
from src.utils.basic_logger import simple_logger as logger
from src.use_cases.exceptions import AIFailedToRespond
from src.entities.message import Message
from typing import Union
import g4f


class AIServiceUseCase:
    def __init__(
        self,
        database_repository: IMessageDBRepository,
        logger: logger,
    ):
        self.database_repository = database_repository
        self.logger = logger
        self._providers = [
            g4f.Provider.Aichat,
            g4f.Provider.ChatBase,
            g4f.Provider.Bing,
            g4f.Provider.GptGo,
            g4f.Provider.You,
            g4f.Provider.Yqcloud,
        ]

    async def execute(
        self, messages, provider: g4f.Provider.BaseProvider = g4f.Provider.Bing
    ) -> None:
        try:
            response = await g4f.ChatCompletion.create_async(
                model="gpt-4",
                messages=messages,
                provider=provider,
            )
            return response
        except Exception as e:
            raise AIFailedToRespond(e)

    def sync_execute(self, **kwargs) -> None:
        asyncio.run(self.execute(**kwargs))
