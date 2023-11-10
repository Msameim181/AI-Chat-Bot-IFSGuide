from dependencies import container
from lagom import Singleton
from src import config
from src.adapters.authentication_provider.authentication import (
    Authenticate,
    AuthorizProviderConfig,
)
from src.frameworks.api import APIEndpoint
from src.adapters.db.django_orm.repository import DjangoORMRepository
from src.use_cases.interfaces.database import IDBRepository
from src.utils.basic_logger import simple_logger as logger
from src.use_cases.sample import SampleUseCase

# Config
container[logger] = logger("AI-Chat-Bot-IFSGuide-Service-TEST")
container[AuthorizProviderConfig] = Singleton(
    AuthorizProviderConfig(
        server_url=config.authentication_provider_config.SERVER_URL,
        client_id=config.authentication_provider_config.CLIENT_ID,
        realm_name=config.authentication_provider_config.REALM_NAME,
        client_secret_key=config.authentication_provider_config.CLIENT_SECRET_KEY,
        token_url=config.authentication_provider_config.TOKEN_URL,
    )
)
container[Authenticate] = Singleton(Authenticate)

# Database
container[IDBRepository] = Singleton(DjangoORMRepository)

# Use Cases
# Must be added in the order of dependency
container[SampleUseCase] = Singleton(SampleUseCase)

# Subscribers
container[APIEndpoint] = Singleton(APIEndpoint)
