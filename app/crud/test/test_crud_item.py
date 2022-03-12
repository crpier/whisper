import logging

import pytest
from mock import MagicMock

from app.crud import crud_item

mocked_db = MagicMock()
mocked_model = MagicMock()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def crudItemData() -> crud_item.CRUDItem:
    return crud_item.CRUDItem(mocked_model)


@pytest.mark.unit
def test_create_returns_result(crudItemData: crud_item.CRUDItem) -> None:
    res = crudItemData.create_with_owner(
        mocked_db, obj_in=mocked_db, owner_id=mocked_db
    )
    assert res is not None
