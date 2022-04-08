from abc import ABC
from typing import Any, Dict

from app.adapters.station.repository import InMemoryStationRepository
from app.models.domain_model import Station, station_id


class AbstractStationUnitOfWork(ABC):
    pass


class ThreadStationUnitOfWork(AbstractStationUnitOfWork):
    stations = InMemoryStationRepository()
    connections: Dict[str, Any] = {}

    def __enter__(self):
        pass

    def __exit__(self, *_):
        pass

    def add_station(self, station: Station):
        self.stations.create(station)

    def run_station(self, station_id: station_id):
        self.stations.play(station_id)

    def connect_to_broadcast_server(self, station_id: station_id):
        conn: Any = self.connections.get(station_id)
        conn.open()
