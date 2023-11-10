import pytest
from fastapi import status
from fastapi.testclient import TestClient

from dependencies import container
from src import config_dependency_injection_test  # noqa
from src.frameworks.api.entry_point import APIEndpoint
import json

client = TestClient(container[APIEndpoint].rest_api_app)


@pytest.fixture
def request_header():
    response = client.post(
        "login", data={"username": "api@gmail.com", "password": "123456"}
    )
    token = response.json()
    print(response)
    print(token)
    return {"Authorization": token["token_type"] + " " + token["access_token"]}


@pytest.fixture
def api_endpoint():
    return container[APIEndpoint]


@pytest.mark.order(11)
@pytest.mark.asyncio
async def test_01_get_api_docs():
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(11)
@pytest.mark.asyncio
async def test_02_get_api_redoc():
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.order(11)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_04_signup():
    response = client.post(
        "/signup",
        data=json.dumps(
            {
                "name": "API Test User",
                "email": "api@gmail.com",
                "password": "123456",
            }
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert (
        response_json["message"] == "Success, user created. Please login to continue."
    )


@pytest.mark.order(11)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_03_login_check(request_header):
    response = client.get("/service", headers=request_header)
    assert response.status_code == status.HTTP_200_OK


interaction_id = None

@pytest.mark.order(11)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_04_create_interaction(request_header):
    response = client.post("/interaction/create", headers=request_header)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["message"] == "Success, interaction created."
    global interaction_id
    interaction_id = response_json["interaction_id"]


@pytest.mark.order(11)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_05_create_message(request_header):
    response = client.post(
        "/message/create",
        headers=request_header,
        data=json.dumps(
            {
                "interaction_id": interaction_id,
                "message": "Hello World",
            }
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["ai_response"] is not None
    response = client.post(
        "/message/create",
        headers=request_header,
        data=json.dumps(
            {
                "interaction_id": interaction_id,
                "message": "Are you a bot?",
            }
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["ai_response"] is not None


@pytest.mark.order(11)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_05_create_message_failed(request_header):
    response = client.post(
        "/message/create",
        headers=request_header,
        data=json.dumps(
            {
                "interaction_id": 2,
                "message": "Hello World",
            }
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.post(
        "/message/create",
        headers=request_header,
        data=json.dumps(
            {
                "interaction_id": 10,
                "message": "Hello World",
            }
        ),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.order(11)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_06_fetch_all_messages(request_header):
    response = client.get(
        f"/message/fetch_all/{interaction_id}",
        headers=request_header,
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["messages"] is not None
    data_json = json.loads(response_json["messages"])
    assert len(data_json) == 2


@pytest.mark.order(11)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_07_fetch_all_messages_failed(request_header):
    response = client.get(
        "/message/fetch_all/2",
        headers=request_header,
    )
    print(response.content)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.get(
        "/message/fetch_all/10",
        headers=request_header,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.order(11)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_08_fetch_all_interactions(request_header):
    response = client.get(
        "/interaction/fetch_all",
        headers=request_header
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["interactions"] is not None
    data_json = json.loads(response_json["interactions"])
    assert len(data_json) == 1
    assert len(data_json[0]['messages']) == 2