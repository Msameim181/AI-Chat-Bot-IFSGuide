import pytest
from django.db.models import Model


@pytest.fixture
def model() -> Model:
    return None

@pytest.mark.order(2)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_1_insert(model) -> None:
    pass


@pytest.mark.order(2)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_2_update(model) -> None:
    pass


@pytest.mark.order(2)
@pytest.mark.django_db
@pytest.mark.asyncio
async def test_3_delete(model) -> None:
    pass


@pytest.mark.order(2)
@pytest.mark.django_db
def test_4_asgi() -> None:
    from src.adapters.db.django_orm.db import asgi  # noqa


@pytest.mark.order(2)
@pytest.mark.django_db
def test_5_main() -> None:
    from manage import main

    main()
