from app.models.domain_model import User, user_id
from app.schemas import user as user_schema
from app.services import user_uow
from app.core.security import get_password_hash, verify_password
from typing import Optional


def create_user(
    create_obj: user_schema.UserCreate, uow: user_uow.AbstractUnitOfWork
) -> user_id:
    hashed_password = get_password_hash(create_obj.password)
    new_user = User(
        name=create_obj.name, email=create_obj.email, password=hashed_password
    )
    with uow:
        user_id = uow.users.add(new_user)
        uow.commit()
        return user_id


def get_users(uow: user_uow.AbstractUnitOfWork):
    with uow:
        uow.users.get_multi()


def authenticate(
    email: str, password: str, uow: user_uow.AbstractUnitOfWork
) -> Optional[user_id]:
    with uow:
        user = uow.users.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user.id
