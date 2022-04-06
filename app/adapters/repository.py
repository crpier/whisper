from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional
from pydantic.networks import EmailStr

from sqlalchemy.orm import Session

from app.models.domain_model import Song, Station, User, station_id, user_id

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import registry

from app.models.domain_model import User


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
