import pytest
from fastapi import status
from fastapi.testclient import TestClient

from dependencies import container
from src.adapters.authentication_provider import authentication
from src.adapters.authentication_provider.authentication import AuthorizProviderConfig
from src.config import authentication_provider_config
from src import config_dependency_injection_test  # noqa
from src.frameworks.api.entry_point import APIEndpoint
from src.use_cases.interfaces.database import IDBRepository

client = TestClient(container[APIEndpoint].rest_api_app)


@pytest.fixture
def request_header():
    auth = authentication.Authenticate(
        AuthorizProviderConfig(
            server_url=authentication_provider_config.SERVER_URL,
            client_id=authentication_provider_config.CLIENT_ID_AUTH_SERVICE,
            realm_name=authentication_provider_config.REALM_NAME,
            client_secret_key=authentication_provider_config.CLIENT_SECRET_KEY_AUTH_SERVICE,
            token_url=authentication_provider_config.TOKEN_URL,
        )
    )
    token = auth.login(
        authentication_provider_config.TEST_USER,
        authentication_provider_config.TEST_PASS,
    )
    return {"Authorization": token["token_type"] + " " + token["access_token"]}


@pytest.fixture
def api_endpoint():
    return container[APIEndpoint]


@pytest.mark.order(11)
@pytest.mark.asyncio
async def test_1_get_api_docs():
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(11)
@pytest.mark.asyncio
async def test_2_get_api_redoc():
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK
