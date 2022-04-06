from typing import Dict

import pytest
from fastapi.testclient import TestClient
from app import schemas

from app.core.config import settings


@pytest.mark.component
def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


@pytest.mark.component
def test_get_current_user(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert result.get("email") is not None
    assert result.get("id") is not None
    assert result.get("name") is not None
    assert result.get("password") is None
    assert result.get("hashed_password") is None
