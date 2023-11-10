import pytest
from src import config_dependency_injection_test  # noqa
from src.entities import Interaction
from dependencies import container
from datetime import datetime, timezone, timedelta
from dataclasses import asdict
from src.adapters.db.django_orm.repositories import InteractionDBRepository # noqa

@pytest.fixture
def repository() -> InteractionDBRepository:
    return container[InteractionDBRepository]  # noqa


@pytest.fixture
def interaction_entity():
    return Interaction(
        id=None,
        user_id=2,
    )  # noqa


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_1_create(repository, interaction_entity):
    interaction = await repository.create(interaction_entity)
    interactions = await repository.get_all()
    assert len(interactions) == 1
    assert interaction.id == interactions[0].id
    assert interaction.settings == interaction_entity.settings
    assert interaction.user_id == interaction_entity.user_id


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_2_get_all(repository, interaction_entity):
    interactions = await repository.get_all()
    assert len(interactions) == 1
    assert interactions[0].settings == interaction_entity.settings
    interactions = await repository.get_all_by_filters({"user_id": interaction_entity.user_id})
    assert len(interactions) == 1
    assert interactions[0].settings == interaction_entity.settings


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_3_get_filter(repository, interaction_entity):
    interaction = await repository.get({"id": 1})
    assert interaction.user_id == interaction_entity.user_id
    interaction_entity_obj = await repository.model_to_obj(interaction)
    assert interaction_entity_obj.settings == interaction_entity.settings
    assert interaction_entity_obj.created_at != interaction_entity.created_at
    assert interaction_entity_obj.updated_at != interaction_entity.updated_at


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_4_update(repository, interaction_entity):
    interaction = await repository.get({"id": 1})
    assert interaction.user_id == interaction_entity.user_id
    interaction.settings = {
        "model_name": "GPT3.5",
        "role": "System",
        "prompt": "As a helpful IFS therapist chatbot, your role is to guide users through a "
        "simulated IFS session in a safe and supportive manner with a few changes to the exact steps of the IFS model.",
    }
    interaction_updated = await repository.update(interaction)
    assert interaction_updated.settings != interaction_entity.settings
    interaction_entity_obj = await repository.model_to_obj(interaction_updated)
    assert interaction_entity_obj.settings == interaction.settings


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_5_update(repository, interaction_entity):
    interaction = await repository.get({"id": 1})
    assert interaction.user_id == interaction_entity.user_id
    interaction_entity_obj = await repository.model_to_obj(interaction)
    interaction_entity_obj.settings = {
        "model_name": "gpt-3.5-turbo",
        "role": "System",
        "prompt": "As a helpful IFS therapist chatbot, your role is to guide users through a "
        "simulated IFS session in a safe and supportive manner with a few changes to the exact steps of the IFS model.",
    }
    interaction_updated = await repository.update_filter(
        {"id": interaction_entity_obj.id}, interaction_entity_obj
    )
    assert interaction_updated.settings == interaction_entity_obj.settings
    interaction_entity_obj = await repository.model_to_obj(interaction_updated)
    assert interaction_entity_obj.settings != interaction_entity.settings


@pytest.mark.order(3)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_6_delete(repository, interaction_entity):
    interaction = await repository.get({"id": 1})
    assert interaction.user_id == interaction_entity.user_id
    response = await repository.delete(interaction.id)
    assert response[0] >= 1
    assert len(await repository.get_all()) == 0
    interaction = await repository.create(interaction_entity)
    assert len(await repository.get_all()) == 1
