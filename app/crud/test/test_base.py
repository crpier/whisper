import logging

import pytest
from mock import MagicMock

from app.crud.base import CRUDBase
from app.models import Item

mocked_model = MagicMock()
mock_session = MagicMock()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

test_id = 1


@pytest.fixture
def test_base() -> CRUDBase:
    return CRUDBase(Item)


@pytest.mark.unit
def test_get_returns_something(test_base: CRUDBase) -> None:
    res = test_base.get(mock_session, test_id)
    assert res is not None
