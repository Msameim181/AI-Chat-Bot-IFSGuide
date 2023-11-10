import pytest
from src import config_dependency_injection_test  # noqa
from src.entities import Message, RoleType
from dependencies import container
from src.adapters.db.django_orm.repositories import MessageDBRepository # noqa

@pytest.fixture
def repository() -> MessageDBRepository:
    return container[MessageDBRepository]  # noqa


@pytest.fixture
def message_entity():
    return Message(
        id=None,
        interaction_id=2,
        role=RoleType.HUMAN.value,
        content="Hello",
    )  # noqa

@pytest.fixture
def sec_message_entity():
    return Message(
        id=None,
        interaction_id=2,
        role=RoleType.AI.value,
        content="Hello to you too!",
    )  # noqa


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_1_create(repository, message_entity, sec_message_entity):
    message = await repository.create(message_entity)
    sec_message = await repository.create(sec_message_entity)
    messages = await repository.get_all()
    assert len(messages) == 2
    assert message.id == messages[0].id
    assert message.role == RoleType.HUMAN.value
    assert message.content == message_entity.content
    assert message.interaction_id == message_entity.interaction_id


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_2_get_all(repository, message_entity, sec_message_entity):
    messages = await repository.get_all()
    assert len(messages) == 2
    assert messages[0].interaction_id == message_entity.interaction_id
    messages = await repository.get_all_by_filters({"interaction_id": message_entity.interaction_id})
    assert len(messages) == 2
    assert messages[0].content == message_entity.content
    assert messages[1].content == sec_message_entity.content


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_3_get_filter(repository, message_entity):
    message = await repository.get({"id": 1})
    assert message.interaction_id == message_entity.interaction_id
    message_entity_obj = await repository.model_to_obj(message)
    assert message_entity_obj.content == message_entity.content
    assert message_entity_obj.role == RoleType.HUMAN.value
    assert message_entity_obj.created_at != message_entity.created_at
    assert message_entity_obj.updated_at != message_entity.updated_at


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_4_update(repository, message_entity):
    message = await repository.get({"id": 1})
    assert message.interaction_id == message_entity.interaction_id
    message.role = RoleType.AI.value
    message_updated = await repository.update(message)
    assert message_updated.role != message_entity.role
    message_entity_obj = await repository.model_to_obj(message_updated)
    assert message_entity_obj.role == message.role


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_5_update(repository, message_entity):
    message = await repository.get({"id": 1})
    assert message.interaction_id == message_entity.interaction_id
    message_entity_obj = await repository.model_to_obj(message)
    message_entity_obj.role = RoleType.HUMAN.value
    message_updated = await repository.update_filter(
        {"id": message_entity_obj.id}, message_entity_obj
    )
    assert message_updated.role == message_entity_obj.role
    message_entity_obj = await repository.model_to_obj(message_updated)
    assert message_entity_obj.role == message_entity.role


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_6_delete(repository, message_entity, sec_message_entity):
    message = await repository.get({"id": 1})
    assert message.interaction_id == message_entity.interaction_id
    response = await repository.delete(message.id)
    assert response[0] >= 1
    message = await repository.get({"id": 2})
    assert message.interaction_id == message_entity.interaction_id
    response = await repository.delete(message.id)
    assert response[0] >= 1
    assert len(await repository.get_all()) == 0
    message = await repository.create(message_entity)
    message = await repository.create(sec_message_entity)
    assert len(await repository.get_all()) == 2
