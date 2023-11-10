# from src import config_dependency_injection_test  # noqa
# from dependencies import container
# from src.use_cases.sample import SampleUseCase
# import pytest
# from src.use_cases.interfaces.database import IDBRepository


# @pytest.fixture
# def sample_use_case() -> SampleUseCase:
#     return SampleUseCase(
#         database_repository=IDBRepository,
#         logger=container[SampleUseCase].logger,
#     )  # noqa


# @pytest.fixture
# def sample_use_case_ready() -> SampleUseCase:
#     return container[SampleUseCase]  # noqa


# @pytest.mark.order(22)
# @pytest.mark.asyncio
# async def test_1_execute_obj(sample_use_case) -> None:
#     pass


# @pytest.mark.order(22)
# @pytest.mark.asyncio
# async def test_2_execute_obj(sample_use_case_ready) -> None:
#     pass
