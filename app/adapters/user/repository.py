from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic.networks import EmailStr

from sqlalchemy.orm import Session

from app.models.domain_model import User, user_id

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import registry

from app.models.domain_model import User


mapper_registry = registry()

user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(255)),
    Column("email", String(255), unique=True, index=True, nullable=False),
    Column("hashed_password", String(255), nullable=False),
)

mapper_registry.map_imperatively(User, user_table)


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_one_by(self, **kwargs) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: user_id) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotADirectoryError

    @abstractmethod
    def get_multi(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> user_id:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: user_id, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: user_id):
        raise NotImplementedError

    @abstractmethod
    def delete_by_email(self, email: EmailStr):
        raise NotImplementedError

    def to_domain_user(self, user: User) -> User:
        raise NotImplementedError


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_one_by(self, **kwargs) -> Optional[User]:
        user = self.session.query(User).filter_by(**kwargs).first()
        return user

    def get(self, id: user_id):
        user = self.session.query(User).filter_by(id=id).first()
        return user

    def get_by_id(self, id: user_id) -> Optional[User]:
        user = self.session.query(User).filter_by(id=id).first()
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        user = self.session.query(User).filter_by(email=email).first()
        return user

    def get_multi(self):
        users = self.session.query(User).all()
        return users

    def add(self, user: User) -> user_id:
        self.session.add(user)
        self.session.flush()
        return user.id

    def update(self, id: user_id, user: User):
        updated_rows = self.session.query(User).filter_by(id=id).update(user)
        return updated_rows

    def delete(self, id: user_id):
        deleted_rows = self.session.query(User).filter_by(id=id).delete()
        return deleted_rows

    def delete_by_email(self, email: EmailStr):
        deleted_rows = self.session.query(User).filter_by(email=email).delete()
        return deleted_rows

    def to_domain_user(self, user: User) -> User:
        raise NotImplementedError


class FakeUserRepository(AbstractUserRepository):
    def __init__(self) -> None:
        # XXX Would a dictionary be easier to user?
        self.container: List[User] = []

    def get_one_by(self, **kwargs) -> Optional[User]:
        candidates = self.container.copy()
        for key, value in kwargs.items():
            candidates = [
                user for user in candidates if user.__dict__[key] == value
            ]

    def get_by_id(self, id: user_id) -> Optional[User]:
        res = [user for user in self.container if user.id == id]
        return res[0]

    def get_by_email(self, email: str) -> Optional[User]:
        res = [user for user in self.container if user.email == email]
        return res[0]

    def get_multi(self) -> List[User]:
        return self.container

    def add(self, user: User) -> user_id:
        self.container.append(user)
        return user.id

    def update(self, id: user_id, **kwargs):
        user_to_change = self.get_by_id(id)
        for key, value in kwargs.values():
            setattr(user_to_change, key, value)

    def delete(self, id: user_id):
        user_to_del = self.get_by_id(id)
        if user_to_del:
            id_to_del = self.container.index(user_to_del)
            del self.container[id_to_del]

    def delete_by_email(self, email: EmailStr):
        user_to_del = self.get_by_email(email)
        if user_to_del:
            id_to_del = self.container.index(user_to_del)
            del self.container[id_to_del]

    def to_domain_user(self, user: User) -> User:
        raise NotImplementedError
