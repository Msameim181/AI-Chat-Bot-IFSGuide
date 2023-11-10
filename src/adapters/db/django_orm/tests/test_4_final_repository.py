# import pytest
# from src.entities import Payment, CurrencyType, PaymentMethod
# from dependencies import container
# from src.adapters.db.django_orm.repositories import (
#     PlanDBRepository,
#     PaymentDBRepository,
#     TeamDBRepository,
#     UserDBRepository,
#     GroupDBRepository,
#     EventDBRepository,
#     TaskDBRepository,
# )
# import asyncio
# from src.adapters.db.django_orm.core.signals import (
#     FailedDeleteDueToExistingRelationship,
# )


import pytest
from src import config_dependency_injection_test  # noqa
from src.entities import Message, RoleType
from dependencies import container
from src.adapters.db.django_orm.repositories import UserDBRepository # noqa
from src.adapters.db.django_orm.repositories import InteractionDBRepository # noqa
from src.adapters.db.django_orm.repositories import MessageDBRepository # noqa

@pytest.fixture
def user_repository() -> UserDBRepository:
    return container[UserDBRepository]  # noqa

@pytest.fixture
def interaction_repository() -> InteractionDBRepository:
    return container[InteractionDBRepository]  # noqa

@pytest.fixture
def message_repository() -> MessageDBRepository:
    return container[MessageDBRepository]  # noqa


@pytest.mark.order(900)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_1_create(user_repository, interaction_repository, message_repository):
    users = await user_repository.get_all()
    assert len(users) == 1
    interactions = await interaction_repository.get_all()
    assert len(interactions) == 1
    messages = await message_repository.get_all()
    assert len(messages) == 2
    await user_repository.delete(users[0].id)
    users = await user_repository.get_all()
    assert len(users) == 0
    interactions = await interaction_repository.get_all()
    assert len(interactions) == 0
    messages = await message_repository.get_all()
    assert len(messages) == 0


