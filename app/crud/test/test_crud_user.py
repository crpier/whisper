import logging

import pytest
from mock import MagicMock

from app.crud.crud_user import CRUDUser

mocked_model = MagicMock()
mock_session = MagicMock()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

test_id = 1
nonexistent_user = "doesn-exit@example.com"
invalid_pass = "invalid"


@pytest.fixture
def user() -> CRUDUser:
    return CRUDUser(mocked_model)


@pytest.mark.unit
def test_authenticate_invalid(user: CRUDUser) -> None:
    """Test invalid user will not be authenticated"""
    with pytest.raises(Exception):
        user.authenticate(mock_session, email="", password="")
