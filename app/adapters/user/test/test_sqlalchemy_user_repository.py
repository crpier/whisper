from typing import Generator
from pydantic.networks import EmailStr
from pytest import fixture, mark

from app.adapters.user.repository import SqlAlchemyUserRepository
from app.models.domain_model import User
from app.schemas.user import UserCreate
from app.services.user_uow import (
    DEFAULT_SESSION_FACTORY,
    SqlAlchemyUnitOfWork,
    get_sqlalchemy_uow,
)
from app.services.user_services import create_user


@fixture
def repository():
    return SqlAlchemyUserRepository(DEFAULT_SESSION_FACTORY())


@fixture
def uow():
    return get_sqlalchemy_uow()


@fixture
def normal_user(
    uow: SqlAlchemyUnitOfWork, repository: SqlAlchemyUserRepository
) -> Generator[User, None, None]:
    user_to_create = UserCreate(
        name="FakeFakington",
        email=EmailStr("faker@example.com"),
        password="fakepass",
    )
    user_id = create_user(user_to_create, uow=uow)
    user = repository.get_by_id(user_id.id)
    assert user

    yield user

    # TODO: create and use service function
    with uow:
        uow.users.delete(user_id.id)
        uow.commit()


@mark.component
def test_get_by_email(normal_user: User, repository: SqlAlchemyUserRepository):
    actual_user = repository.get_by_email(normal_user.email)
    assert normal_user.__dict__ == actual_user.__dict__
