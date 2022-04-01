from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from app import models, schemas
from app.core.config import settings
from app.services import user_services
from app.services.user_uow import SqlAlchemyUnitOfWork, get_sqlalchemy_uow
from app.utils import send_new_account_email
from app.models.domain_model import User, user_id

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    user_uow: SqlAlchemyUnitOfWork = Depends(get_sqlalchemy_uow),
) -> Any:
    """
    Retrieve users.
    """
    users = user_services.get_users(user_uow)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    user_in: schemas.UserCreate,
    _: models.User = Depends(user_services.get_current_user),
    user_uow: SqlAlchemyUnitOfWork = Depends(get_sqlalchemy_uow),
) -> User:
    """
    Create new user.
    """
    try:
        user = user_services.create_user(user_in, user_uow)
    except user_services.DuplicateException:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email,
            username=user_in.email,
            password=user_in.password,
        )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(user_services.get_current_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(user_services.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(
        password=password, email=email, full_name=full_name
    )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: user_id,
    user_uow: SqlAlchemyUnitOfWork = Depends(get_sqlalchemy_uow),
    current_user: models.User = Depends(user_services.get_current_user),
) -> Any:
    """
    Get a specific user by id.
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )

    user = user_services.get_user_by_id(user_id, user_uow)
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(user_services.get_current_user),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
