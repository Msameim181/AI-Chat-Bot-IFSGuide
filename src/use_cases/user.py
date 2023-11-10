from src.use_cases.interfaces.database import IUserDBRepository
import asyncio
from src.utils.basic_logger import simple_logger as logger
from src.entities.user import User
from src.use_cases.exceptions import UserNotAuthorized, UserNotFound
from typing import Union, List
import bcrypt


class UserUseCase:
    def __init__(
        self,
        database_repository: IUserDBRepository,
        logger: logger,
    ):
        self.database_repository = database_repository
        self.logger = logger

    async def execute(self, **kwargs) -> None:
        pass

    def sync_execute(self, **kwargs) -> None:
        asyncio.run(self.execute(**kwargs))

    async def password_hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    async def password_check(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    async def add_new_user(self, user: User) -> Union[User, None]:
        user.password = await self.password_hash(user.password)
        response = await self.database_repository.create(user)
        if response is None or not response:
            return None
        return await self.database_repository.model_to_obj(response)

    async def get_user_by_id(self, id: str) -> User:
        user = await self.database_repository.get_by_id(id)
        if user is None or not user:
            return None
        return await self.database_repository.model_to_obj(user)

    async def get_all_users(self) -> List[User]:
        users = await self.database_repository.get_all()
        if users is None or not users:
            return None
        return [await self.database_repository.model_to_obj(user) for user in users]

    async def get_user_by_email(self, email: str) -> User:
        user = await self.database_repository.get({"email": email})
        if user is None or not user:
            return None
        return await self.database_repository.model_to_obj(user)

    async def update_user(self, user: User) -> Union[User, None]:
        if user.password is not None:
            user.password = await self.password_hash(user.password)
        response = await self.database_repository.update_filter({"id": user.id}, user)
        if response is None or not response:
            return None
        return await self.database_repository.model_to_obj(response)

    async def delete_user(self, id: str) -> bool:
        response = await self.database_repository.delete(id)
        return bool(
            response is not None and (not isinstance(response, tuple) or response[0])
        )

    async def user_login(self, email: str, password: str) -> Union[User, None]:
        user = await self.database_repository.get({"email": email})
        if user is None or not user:
            raise UserNotFound("User with provided email does not exist")
        if not await self.password_check(password, user.password):
            raise UserNotAuthorized("Password does not match")
        return await self.database_repository.model_to_obj(user)
