from abc import ABC, abstractmethod

from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.adapters.repository import (
    AbstractUserRepository,
    SqlAlchemyUserRepository,
)
from app.core.config import settings

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(settings.SQLALCHEMY_DATABASE_URI)
)


class AbstractUnitOfWork(ABC):
    users: AbstractUserRepository

    def __enter__(self):
        return self

    def __exit__(self):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.user_repo = SqlAlchemyUserRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


@lru_cache
def get_sqlalchemy_uow():
    return SqlAlchemyUnitOfWork()
