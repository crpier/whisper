from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session

from app.models.domain_model import (
    Playlist,
    Song,
    Station,
    User,
    station_id,
    user_id,
)


class AbstractSongRepository(ABC):
    @abstractmethod
    def get(self, title, album, artist) -> Song:
        raise NotImplementedError

    @abstractmethod
    def download(self, song: Song) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def add(self, song: Song) -> bool:
        raise NotImplementedError


class AbstractUserRepository(ABC):
    @abstractmethod
    def get(self) -> User:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, title, album, artist, song: Song):
        raise NotImplementedError


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, id: user_id):
        user = self.session.query(User).filter_by(id=id).first()
        return user

    def add(self, user: User):
        self.session.add(user)

    def update(self, id: user_id, user: User):
        updated_rows = self.session.query(User).filter_by(id=id).update(user)
        return updated_rows

    def delete(self, id: user_id):
        deleted_rows = self.session.query(User).filter_by(id=id).delete()
        return deleted_rows


class AbstractPlaylistRepository(ABC):
    @abstractmethod
    def get(self, id) -> Playlist:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: Playlist) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, owner, id, song: Playlist):
        raise NotImplementedError


class AbstractStationRepository(ABC):
    @abstractmethod
    def get(self, id: station_id) -> Station:
        raise NotImplementedError

    @abstractmethod
    def add(self, station: Station):
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Station]:
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, user_id: user_id) -> List[Station]:
        raise NotImplementedError
