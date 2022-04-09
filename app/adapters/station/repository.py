from abc import ABC
from typing import Dict, Generic, List, Tuple, TypeVar
from app.models.domain_model import Station, station_id


class AbstractStationRepository(ABC):
    pass


T = TypeVar("T")

# TODO investigate how to handle the threads
# from copy import deepcopy
deepcopy = lambda x: x

class InMemoryStationRepository(Generic[T], AbstractStationRepository):
    def __init__(self) -> None:
        self._container: Dict[str, Tuple[Station, T]] = {}

    def add(self, aggregate: Tuple[Station, T]) -> Tuple[Station, T]:
        station_id = aggregate[0].id
        if self._container.get(station_id) is not None:
            raise StationAlreadyExists
        self._container[station_id] = aggregate
        return deepcopy(aggregate)

    def get_all_stations(self) -> List[Station]:
        return [deepcopy(station) for (station, _) in self._container.values()]

    def get_station(self, station_id: station_id) -> Station:
        station, _ = self._container[station_id]
        copy = deepcopy(station)
        return copy

    def get_meta(self, station_id: station_id):
        _, meta = self._container[station_id]
        return meta

    def get(self, station_id: station_id) -> Tuple[Station, T]:
        source_aggregate = self._container.get(station_id)
        if source_aggregate is None:
            raise StationDoesNotExist
        copy = deepcopy(source_aggregate)
        return copy

    def remove(self, station_id: station_id):
        if self._container.get(station_id) is None:
            raise StationDoesNotExist
        del self._container[station_id]

class StationDoesNotExist(BaseException):
    pass


class StationAlreadyExists(BaseException):
    pass
