from pydantic.networks import EmailStr
from app.models.domain_model import User, user_id
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
        name=create_obj.name, email=create_obj.email, hashed_password=hashed_password
    )
    with uow:
        user_id = uow.users.add(new_user)
        db_user = uow.users.get_by_id(user_id)
        user = User(**db_user.__dict__)
        uow.commit()
    return user

def get_user_by_email(email: EmailStr, uow: user_uow.AbstractUnitOfWork) -> Optional[User]:
    with uow:
        db_user = uow.users.get_one_by(email=email)
        if not db_user:
            return
        user = User(**db_user.__dict__)
        return user
        

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


def get_current_user(
         uow: user_uow.AbstractUnitOfWork = Depends(user_uow.get_sqlalchemy_uow), token: str = Depends(reusable_oauth2)
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
        return schemas.User(**user.__dict__)

class InvalidCredentials(BaseException):
    pass

class UserNotFound(BaseException):
    pass
