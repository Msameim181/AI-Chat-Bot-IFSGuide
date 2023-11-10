from src import config_dependency_injection_test  # noqa
from dependencies import container
from src.use_cases.interaction import InteractionUseCase
import pytest
from src.entities import Interaction


@pytest.fixture
def use_case() -> InteractionUseCase:
    return container[InteractionUseCase]  # noqa


@pytest.fixture
def interaction_entity():
    return Interaction(
        id=None,
        user_id=2,
    )  # noqa


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_1_create(use_case, interaction_entity) -> None:
    response = await use_case.add_new_interaction(interaction_entity)
    assert response is not None
    assert response.settings == interaction_entity.settings
    assert response.user_id == interaction_entity.user_id


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_2_get_interaction_by_id(use_case, interaction_entity) -> None:
    response = await use_case.get_interaction_by_id(3)
    assert response is not None
    assert response.user_id == interaction_entity.user_id


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_3_get_all_interactions(use_case, interaction_entity) -> None:
    response = await use_case.get_all_interactions()
    assert response is not None
    assert len(response) == 2


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_4_get_interaction_by_name(use_case, interaction_entity) -> None:
    response = await use_case.get_interaction_by_user_id(2)
    assert response is not None
    assert response.settings == interaction_entity.settings


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_5_update_interaction(use_case, interaction_entity) -> None:
    interaction = Interaction(id=3, user_id=None, settings={})  # noqa
    response = await use_case.update_interaction(interaction)
    assert response is not None
    assert response.user_id == interaction_entity.user_id
    assert response.settings != interaction_entity.settings


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_6_update_interaction(use_case, interaction_entity) -> None:
    interaction = Interaction(id=3, user_id=None, settings=None)  # noqa
    response = await use_case.update_interaction(interaction)
    assert response is not None
    assert response.user_id == interaction_entity.user_id
    assert response.settings == {}


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_7_get_interaction_failed(use_case, interaction_entity) -> None:
    response = await use_case.get_interaction_by_id(6)
    assert response is None
    response = await use_case.get_interaction_by_user_id(2)
    assert response is not None


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_8_delete_interaction(use_case, interaction_entity) -> None:
    response = await use_case.delete_interaction(3)
    assert response is True
    response = await use_case.delete_interaction(3)
    assert response is False
    response = await use_case.get_interaction_by_id(3)
    assert response is None


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_9_retrieve_all(use_case) -> None:
    response = await use_case.retrieve_all(2)
    assert response is not None
    print(response)
    assert len(response) == 1
