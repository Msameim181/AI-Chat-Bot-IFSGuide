# import pytest
# from src.adapters.db.django_orm.core.models import *
# from src.entities import *
# from dependencies import container
# from datetime import datetime, timezone, timedelta
# from dataclasses import asdict
# from src.adapters.db.django_orm.repository import DjangoORMRepository


# @pytest.fixture
# def repository_source() -> DjangoORMRepository:
#     return DjangoORMRepository(logger=container[DjangoORMRepository].logger)  # noqa


# @pytest.fixture
# def repository() -> DjangoORMRepository:
#     return container[DjangoORMRepository]  # noqa


# @pytest.fixture
# def entity_model():
#     return True


# @pytest.mark.order(3)
# @pytest.mark.django_db
# @pytest.mark.asyncio
# async def test_1_save(repository, entity_model):
#     pass
