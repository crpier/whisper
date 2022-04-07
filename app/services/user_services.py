from pydantic.networks import EmailStr
from sqlalchemy.exc import IntegrityError
from app.models.domain_model import Station, User, user_id, Playlist
from app import schemas
from app.schemas import user as user_schema
from app.services import user_uow
from app.core.security import get_password_hash, verify_password
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from fastapi import Depends
from jose import jwt
from app.core import security

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app import schemas
from app.core import security
from app.core.config import settings


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def create_user(
    create_obj: user_schema.UserCreate, uow: user_uow.AbstractUnitOfWork
) -> User:
    hashed_password = get_password_hash(create_obj.password)
    new_user = User(
        name=create_obj.name,
        email=create_obj.email,
        hashed_password=hashed_password,
    )
    try:
        with uow:
            new_id = uow.users.add(new_user)
            uow.commit()
            # TODO: check if this can be better achieved by adding the object and calling session.refresh()
            created_user = uow.users.get_by_id(new_id)
            assert created_user
    except IntegrityError:
        raise DuplicateException
    return created_user


def get_user_by_email(
    email: EmailStr, uow: user_uow.AbstractUnitOfWork
) -> Optional[User]:
    with uow:
        user = uow.users.get_one_by(email=email)
        if not user:
            return
        return user


def get_user_by_id(
    id: user_id, uow: user_uow.AbstractUnitOfWork
) -> Optional[User]:
    with uow:
        user = uow.users.get_one_by(id=id)
        if not user:
            return
        return user


def get_users(uow: user_uow.AbstractUnitOfWork):
    with uow:
        users = uow.users.get_multi()
        return users


def authenticate(
    email: str, password: str, uow: user_uow.AbstractUnitOfWork
) -> Optional[user_id]:
    with uow:
        user = uow.users.get_by_email(email=email)
        uow.commit()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user.id


def get_current_user(
    uow: user_uow.AbstractUnitOfWork = Depends(user_uow.get_sqlalchemy_uow),
    token: str = Depends(reusable_oauth2),
) -> schemas.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise InvalidCredentials
    with uow:
        id = user_id(str(token_data.sub))
        user = uow.users.get_by_id(id)
        if not user:
            raise UserNotFound
        return_user = schemas.User(**user.__dict__)
        uow.commit()
    return return_user


def change_user_tier(
    user_id: user_id,
    tier: str,
    uow: user_uow.AbstractUnitOfWork = Depends(user_uow.get_sqlalchemy_uow),
):
    raise NotImplementedError

class InvalidCredentials(BaseException):
    pass


class UserNotFound(BaseException):
    pass


class DuplicateException(BaseException):
    pass
