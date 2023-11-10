from src import config_dependency_injection_test  # noqa
from dependencies import container
from src.use_cases.message import MessageUseCase
from src.use_cases.ai_service import AIServiceUseCase
import pytest
from src.entities import Message, RoleType
import traceback


@pytest.fixture
def use_case() -> AIServiceUseCase:
    return container[AIServiceUseCase]  # noqa


@pytest.fixture
def message_use_case() -> MessageUseCase:
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
async def test_01_create(use_case) -> None:
    try:
        response = await use_case.execute(
            messages=[{"role": "user", "content": "Hello"}],
        )
        print(response)
        assert response is not None
    except Exception as e:
        print(e)
        assert False


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_02_create_real_conversion(message_use_case, message_entity) -> None:
    try:
        response = await message_use_case.add_new_message(
            message_entity, 2, will_ai_respond=True
        )
        assert response is not None
        assert response.role == RoleType.AI.value
        print(response)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        assert False
