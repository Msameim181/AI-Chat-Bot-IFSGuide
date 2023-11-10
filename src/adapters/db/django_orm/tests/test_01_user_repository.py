import pytest
from src import config_dependency_injection_test  # noqa
from src.entities import User
from dependencies import container
from datetime import datetime, timezone, timedelta
from dataclasses import asdict
from src.adapters.db.django_orm.repositories import UserDBRepository # noqa

@pytest.fixture
def repository() -> UserDBRepository:
    return container[UserDBRepository]  # noqa


@pytest.fixture
def user_entity():
    return User(
        id=None,
        name="Test User",
        email="sample@gmail.com",
        password="123456",
        is_verified=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )  # noqa


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_1_create(repository, user_entity):
    user = await repository.create(user_entity)
    users = await repository.get_all()
    assert len(users) == 1
    assert user.id == users[0].id
    assert user.name == user_entity.name
    assert user.email == user_entity.email
    assert user.password == user_entity.password


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_2_get_all(repository, user_entity):
    users = await repository.get_all()
    assert len(users) == 1
    assert users[0].name == user_entity.name
    users = await repository.get_all_by_filters({"is_verified": user_entity.is_verified})
    assert len(users) == 1
    assert users[0].name == user_entity.name


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_3_get_filter(repository, user_entity):
    user = await repository.get({"email": user_entity.email})
    assert user.name == user_entity.name
    user_entity_obj = await repository.model_to_obj(user)
    assert user_entity_obj.name == user_entity.name
    assert user_entity_obj.created_at != user_entity.created_at
    assert user_entity_obj.updated_at != user_entity.updated_at


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_4_update(repository, user_entity):
    user = await repository.get({"email": user_entity.email})
    assert user.name == user_entity.name
    user.password = "56789"
    user_updated = await repository.update(user)
    assert user_updated.password == "56789"
    user_entity_obj = await repository.model_to_obj(user_updated)
    assert user_entity_obj.name == user_entity.name


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_5_update(repository, user_entity):
    user = await repository.get({"email": user_entity.email})
    assert user.name == user_entity.name
    user_entity_obj = await repository.model_to_obj(user)
    user_entity_obj.is_verified = True
    user_updated = await repository.update_filter(
        {"id": user_entity_obj.id}, user_entity_obj
    )
    assert user_updated.is_verified == user_entity_obj.is_verified
    user_entity_obj = await repository.model_to_obj(user_updated)
    assert user_entity_obj.name == user_entity.name


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_6_delete(repository, user_entity):
    user = await repository.get({"email": user_entity.email})
    assert user.name == user_entity.name
    response = await repository.delete(user.id)
    assert response[0] >= 1
    assert len(await repository.get_all()) == 0
    user = await repository.create(user_entity)
    assert len(await repository.get_all()) == 1
