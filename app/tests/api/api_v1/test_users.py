from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.services.user_uow import SqlAlchemyUnitOfWork, get_sqlalchemy_uow
from app.tests.utils.utils import random_email, random_lower_string
from app.services import user_services


@pytest.mark.component
def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL


@pytest.mark.component
def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["email"] == settings.TEST_USER_EMAIL


@pytest.mark.component
def test_create_user_new_email(
        client: TestClient, superuser_token_headers: dict, uow: SqlAlchemyUnitOfWork = get_sqlalchemy_uow()
) -> None:
    email = random_email()
    name = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "password": password, "name": name}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = user_services.get_user_by_email(email, uow)
    assert user
    assert user.email == created_user["email"]
    assert user.id == created_user["id"]
    assert user.id is not None

    # Ensure we don't expose passwords
    assert created_user.get("hashed_password") is None
    assert created_user.get("password") is None


@pytest.mark.component
def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, uow: SqlAlchemyUnitOfWork = get_sqlalchemy_uow()
) -> None:
    email = random_email()
    name = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, name=name, password=password)
    user = user_services.create_user(user_in, uow)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = user_services.get_user_by_email(email, uow)
    assert existing_user
    assert existing_user.email == api_user["email"]


@pytest.mark.component
def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, uow: SqlAlchemyUnitOfWork = get_sqlalchemy_uow()
) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, name=username, password=password)
    user_services.create_user(user_in, uow)
    data = {"email": email, "password": password, "name": username}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user

@pytest.mark.component
def test_create_user_by_super_user(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    email = random_email()
    username = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password, "name": username}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200



@pytest.mark.component
@pytest.mark.skip("superuser functionality not implemented")
def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    email = random_email()
    username = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password, "name": username}
    r = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 400


@pytest.mark.component
def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, uow: SqlAlchemyUnitOfWork = get_sqlalchemy_uow()
) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, name=username, password=password)
    user_services.create_user(user_in, uow)

    email2 = random_email()
    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=email2, name=username2, password=password2)

    r = client.get(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers
    )
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
        assert "name" in item
        assert "password" not in item
