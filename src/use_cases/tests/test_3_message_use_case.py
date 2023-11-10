from src import config_dependency_injection_test  # noqa
from dependencies import container
from src.use_cases.message import MessageUseCase
import pytest
from src.entities import Message, RoleType


@pytest.fixture
def use_case() -> MessageUseCase:
    return container[MessageUseCase]  # noqa


@pytest.fixture
def message_entity():
    return Message(
        id=None,
        interaction_id=2,
        role=RoleType.HUMAN.value,
        content="What is your name?",
    )  # noqa


item_id = None


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_01_create(use_case, message_entity) -> None:
    response = await use_case.add_new_message(message_entity, 2)
    assert response is not None
    assert response.content == message_entity.content
    assert response.role == message_entity.role
    global item_id
    item_id = response.id


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_02_get_message_by_id(use_case, message_entity) -> None:
    response = await use_case.get_message_by_id(item_id)
    assert response is not None
    assert response.content == message_entity.content


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_03_get_all_messages(use_case, message_entity) -> None:
    response = await use_case.get_all_messages()
    assert response is not None
    assert len(response) == 3


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_04_update_message(use_case, message_entity) -> None:
    message = Message(
        id=item_id,
        interaction_id=2,
        role=RoleType.HUMAN.value,
        content="What's your name?",
    )  # noqa
    response = await use_case.update_message(message)
    assert response is not None
    assert response.role == message_entity.role
    assert response.content != message_entity.content


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_06_update_message(use_case, message_entity) -> None:
    message = Message(
        id=item_id,
        interaction_id=None,
        role=None,
        content="What is your owner's name?",
    )  # noqa
    response = await use_case.update_message(message)
    assert response is not None
    assert response.role == message_entity.role
    assert response.content == "What is your owner's name?"
    assert response.content != message_entity.content


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_07_get_message_failed(use_case, message_entity) -> None:
    response = await use_case.get_message_by_id(6)
    assert response is None
    response = await use_case.get_messages_by_interaction_id(6)
    assert response is None


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_08_retrieve_all(use_case, message_entity) -> None:
    response = await use_case.retrieve_all(2, 2)
    assert response is not None
    assert len(response) == 3


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_09_retrieve_all_failed(use_case, message_entity) -> None:
    try:
        response = await use_case.retrieve_all(6, 2)
    except Exception as InteractionNotFound:
        assert True
    try:
        response = await use_case.retrieve_all(2, 6)
    except Exception as UserNotAuthorized:
        assert True


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_10_delete_message(use_case, message_entity) -> None:
    response = await use_case.delete_message(item_id)
    assert response is True
    response = await use_case.delete_message(item_id)
    assert response is False
    response = await use_case.get_message_by_id(item_id)
    assert response is None
