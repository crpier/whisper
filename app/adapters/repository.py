from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional

from sqlalchemy.orm import Session

from app.models.domain_model import Song, Station, User, station_id, user_id


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
    def get_by_id(self) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotADirectoryError

    @abstractmethod
    def get_multi(self) -> User:
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

    def get_by_email(self, email: str) -> Optional[User]:
        user = self.session.query(User).filter_by(email=email).first()
        return user

    def get_multi(self):
        users = self.session.query(User).all()
        return users

    def add(self, user: User):
        self.session.add(user)

    def update(self, id: user_id, user: User):
        updated_rows = self.session.query(User).filter_by(id=id).update(user)
        return updated_rows

    def delete(self, id: user_id):
        deleted_rows = self.session.query(User).filter_by(id=id).delete()
        return deleted_rows


class AbstractStationRepository(ABC):
    @abstractmethod
    def get(self, id: station_id) -> Station:
        raise NotImplementedError

    @abstractmethod
    def create(self, station: Station):
        raise NotImplementedError

    @abstractmethod
    def get_all_stations(self) -> List[Station]:
        raise NotImplementedError

    @abstractmethod
    def get_stations_by_user(self, user_id: user_id) -> List[Station]:
        raise NotImplementedError

    @abstractmethod
    def remove(self, station: Station):
        raise NotImplementedError

class ThreadStationRepository(AbstractStationRepository):
    def __init__(self) -> None:
        self._container: Dict[str, Station] = {}

    @classmethod
    def make_container_key(cls, user_id: user_id, station_id: station_id):
        return user_id + station_id

    def create(self, user_id: user_id, station: Station):
        key = self.make_container_key(user_id, station.id)
        if self._container.get(key) is not None:
            return StationAlreadyExists

    def get_all_stations(self):
        return list(self._container)

    def get_stations_by_user(self, user_id: user_id):
        result: List[Tuple[str, Station]] = []
        for key in self._container.keys():
            if key.startswith(user_id):
                result.append((key, self._container.get(key)))  # type: ignore
        return result

    def remove(self, station: Station):
        key = self.make_container_key(station.owner_id, station.id)
        del self._container[key]


class StationAlreadyExists(BaseException):
    pass
