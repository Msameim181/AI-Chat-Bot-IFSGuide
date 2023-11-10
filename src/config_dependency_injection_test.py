from dependencies import container
from lagom import Singleton
from src import config

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

# from src.use_cases.sample import SampleUseCase

# Config
container[logger] = logger("AI-Chat-Bot-IFSGuide-Service-TEST")

# Database
container[IUserDBRepository] = Singleton(UserDBRepository)
container[IInteractionDBRepository] = Singleton(InteractionDBRepository)
container[IMessageDBRepository] = Singleton(MessageDBRepository)

# Use Cases
# Must be added in the order of dependency
# container[SampleUseCase] = Singleton(SampleUseCase)

# Subscribers
container[APIEndpoint] = Singleton(APIEndpoint)
