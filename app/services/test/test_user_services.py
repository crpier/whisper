from pydantic.networks import EmailStr
from pytest import fixture
from app.core.security import get_password_hash

from app.services.user_uow import FakeUnitOfWork
from app.services.user_services import create_user

from app.schemas.user import UserCreate


class TestCreateUser:
    @fixture(scope="class")
    def fake_uow(self):
        return FakeUnitOfWork()

    @fixture(scope="class")
    def normal_user(self):
        return UserCreate(
            name="Fake Fakington",
            email=EmailStr("fakeman@example.com"),
            password="securepassword",
        )

    def test_password_is_not_added_as_is(
        self, fake_uow: FakeUnitOfWork, normal_user: UserCreate
    ):
        new_user = create_user(normal_user, fake_uow)
        assert normal_user.password != new_user.hashed_password
