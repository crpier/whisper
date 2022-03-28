from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import base, session
from app.schemas.user import UserCreate  # noqa: F401
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

    user_in = UserCreate(
        email=settings.FIRST_SUPERUSER_EMAIL,
        name=settings.FIRST_SUPERUSER_NAME,
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )
    user_services.create_user(create_obj=user_in, uow=get_sqlalchemy_uow())
