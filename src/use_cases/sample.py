from src.use_cases.interfaces.database import IDBRepository
import asyncio
from src.utils.basic_logger import simple_logger as logger


class SampleUseCase:
    def __init__(
        self,
        database_repository: IDBRepository,
        logger: logger,
    ):
        self.database_repository = database_repository
        self.logger = logger

    async def execute(self, **kwargs) -> None:
        pass

    def sync_execute(self, **kwargs) -> None:
        asyncio.run(self.execute_job(**kwargs))

    async def main(self):
        self.logger.info("Starting main process...")