from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base, session  # noqa: F401
from app.services.user_uow import get_sqlalchemy_uow
from app.services import user_services

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # TODO make this depend on config
    base.Base.metadata.create_all(bind=session.engine)

    user_in = schemas.UserCreate(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )
    user_services.create_user(create_obj=user_in, uow=get_sqlalchemy_uow())
