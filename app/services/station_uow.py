from abc import ABC
from typing import Any, Dict

import shout
from app.adapters.station.repository import InMemoryStationRepository
from app.models.domain_model import Station, station_id


class AbstractStationUnitOfWork(ABC):
    pass


class ThreadStationUnitOfWork(AbstractStationUnitOfWork):
    stations = InMemoryStationRepository()
    connections: Dict[str, Any] = {}

    def __enter__(self):
        pass

    def __exit__(self):
        pass

    def register_connection(self, station: Station):
        conn = shout.Shout()
        conn.host = station.broadcastServer.hostname
        conn.port = station.broadcastServer.port
        conn.user = station.broadcastServer.user
        conn.password = station.broadcastServer.password
        conn.format = "mp3"

        conn.name = station.name
        conn.mount = f"/{station.id}"
        conn.genre = station.genre
        conn.description = station.description

        self.connections[station.id] = conn

    def connect_to_server(self, station_id: station_id):
        conn: Any = self.connections.get(station_id)
        conn.open()
