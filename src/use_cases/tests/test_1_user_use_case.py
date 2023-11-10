from src import config_dependency_injection_test  # noqa
from dependencies import container
from src.use_cases.user import UserUseCase
import pytest
from src.entities import User


@pytest.fixture
def use_case() -> UserUseCase:
    return container[UserUseCase]  # noqa


@pytest.fixture
def user_entity():
    return User(
        id=None,
        name="Test User",
        email="example@gmail.com",
        password="123456",
        is_verified=False,
    )  # noqa


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_01_create(use_case, user_entity) -> None:
    response = await use_case.add_new_user(user_entity)
    assert response is not None
    assert response.name == user_entity.name


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_02_get_user_by_id(use_case, user_entity) -> None:
    response = await use_case.get_user_by_id(3)
    assert response is not None
    assert response.email == user_entity.email


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_03_get_all_users(use_case, user_entity) -> None:
    response = await use_case.get_all_users()
    assert response is not None
    assert len(response) == 2


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_04_get_user_by_name(use_case, user_entity) -> None:
    response = await use_case.get_user_by_email("example@gmail.com")
    assert response is not None
    assert response.name == user_entity.name
    assert await use_case.password_check("123456", response.password) is True


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_05_update_user(use_case, user_entity) -> None:
    user = User(
        id=3,
        name=None,
        email=None,
        password="951753",
        is_verified=None,
    )  # noqa
    response = await use_case.update_user(user)
    assert response is not None
    assert response.name == user_entity.name
    assert response.is_verified is False
    assert await use_case.password_check("123456", response.password) is False
    assert await use_case.password_check("951753", response.password) is True


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_06_update_user(use_case, user_entity) -> None:
    user = User(
        id=3,
        name=None,
        email=None,
        password=None,
        is_verified=True,
    )  # noqa
    response = await use_case.update_user(user)
    assert response is not None
    assert response.name == user_entity.name
    assert response.is_verified is True
    assert await use_case.password_check("123456", response.password) is False
    assert await use_case.password_check("951753", response.password) is True


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_07_get_user_failed(use_case, user_entity) -> None:
    response = await use_case.get_user_by_id(6)
    assert response is None
    response = await use_case.get_user_by_email("x@gmail.com")
    assert response is None
    response = await use_case.add_new_user(user_entity)
    assert response is None
    user = User(
        id=10,
        name=None,
        email=None,
        password=None,
        is_verified=True,
    )  # noqa
    response = await use_case.update_user(user)
    assert response is None


@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_08_user_login(use_case, user_entity) -> None:
    response = await use_case.user_login(
        email="example@gmail.com",
        password="951753",
    )
    assert response is not None
    assert response.name == user_entity.name

@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_09_user_login_failed(use_case, user_entity) -> None:
    try:
        await use_case.user_login(
            email="example@gmail.com",
            password="123456",
        )
    except Exception as UserNotAuthorized:
        assert True
    try:
        await use_case.user_login(
            email="loop@gmail.com",
            password="123456",
        )
    except Exception as UserNotFound:
        assert True
        



@pytest.mark.order(10)
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_10_delete_user(use_case, user_entity) -> None:
    response = await use_case.delete_user(3)
    assert response is True
    response = await use_case.delete_user(3)
    assert response is False
    response = await use_case.get_user_by_id(3)
    assert response is None
