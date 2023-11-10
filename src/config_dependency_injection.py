from dependencies import container
from lagom import Singleton

from src.frameworks.api import APIEndpoint
from src.utils.basic_logger import simple_logger as logger
from src.adapters.db.django_orm.repositories import (
    UserDBRepository,
    InteractionDBRepository,
    MessageDBRepository,
)
from src.use_cases.interfaces.database import (
    IUserDBRepository,
    IInteractionDBRepository,
    IMessageDBRepository,
)
from src.use_cases import (
    UserUseCase,
    InteractionUseCase,
    MessageUseCase,
    AIServiceUseCase,
)


# Config
container[logger] = logger("AI-Chat-Bot-IFSGuide-Service-TEST")

# Database
container[IUserDBRepository] = Singleton(UserDBRepository)
container[IInteractionDBRepository] = Singleton(InteractionDBRepository)
container[IMessageDBRepository] = Singleton(MessageDBRepository)

# Use Cases
# Must be added in the order of dependency
container[UserUseCase] = Singleton(UserUseCase)
container[InteractionUseCase] = Singleton(InteractionUseCase)
container[MessageUseCase] = Singleton(MessageUseCase)
container[AIServiceUseCase] = Singleton(AIServiceUseCase)

# Subscribers
container[APIEndpoint] = Singleton(APIEndpoint)
