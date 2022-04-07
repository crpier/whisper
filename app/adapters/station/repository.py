import json
from abc import ABC
from typing import Any, Dict, List, Tuple

from app.models.domain_model import BroadcastServer, Station, station_id, user_id


class AbstractStationRepository(ABC):
    pass

class InMemoryStationRepository(AbstractStationRepository):
    def __init__(self) -> None:
        self._container: Dict[str, Station] = {}

    def create(self, station: Station):
        if self._container.get(station.id) is not None:
            return StationAlreadyExists
        self._container[station.id] = station

    def get_all(self) -> Dict[str, Station]:
        return self._container

    def get_stations_by_user_id(self, user_id: user_id):
        result: List[Tuple[str, Station]] = []
        for key in self._container.keys():
            if key.startswith(user_id):
                result.append((key, self._container.get(key)))  # type: ignore
        return result
    
    def get(self, station_id: station_id) -> Station:
        return self._container[station_id]

    def remove(self, station: Station):
        if self._container.get(station.id) is None:
            raise StationDoesNotExist
        del self._container[station.id]

class StationAlreadyExists(BaseException):
    pass

class StationDoesNotExist(BaseException):
    pass
