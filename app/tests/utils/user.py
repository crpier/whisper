from typing import Dict

from fastapi.testclient import TestClient
from pydantic.networks import EmailStr

from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_lower_string
from app.services.user_uow import get_sqlalchemy_uow, SqlAlchemyUnitOfWork
from app.services import user_services


def user_authentication_headers(
    *, client: TestClient, email: EmailStr, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(
        *, client: TestClient, email: EmailStr, uow: SqlAlchemyUnitOfWork = get_sqlalchemy_uow()
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    with uow:
        user = user_services.get_user_by_email(email, uow)
        if not user:
            user_in = UserCreate(name=email, email=email, password=password)
            user = user_services.create_user(user_in, uow)

        return user_authentication_headers(
            client=client, email=email, password=password
        )
