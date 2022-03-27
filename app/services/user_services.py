from app.models.domain_model import User
from app.schemas import user as user_schema
from app.services import user_uow
from app.core.security import verify_password
from typing import Optional


def create_user(create_obj: user_schema.UserCreate, uow: user_uow.AbstractUnitOfWork):
    with uow:
       uow.users.add(create_obj)
       uow.commit()
    return user_schema.User(**db_obj.__dict__)

def get_users(uow: user_uow.AbstractUnitOfWork):
    with uow:
        uow.users.get_multi()

def authenticate(email: str, password: str, uow: user_uow.AbstractUnitOfWork) -> Optional[User]:
    with uow:
        user = uow.users.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
