from abc import ABC
from queue import Queue
from typing import Dict, List, Tuple
from threading import Thread
from pathlib import Path
import sys
import shout
from app.models.domain_model import Station, station_id, user_id

temp_queue = Queue()
temp_queue.put("/home/crpier/Downloads/music/1.mp3")
temp_queue.put("/home/crpier/Downloads/music/2.mp3")
temp_queue.put("/home/crpier/Downloads/music/3.mp3")
temp_queue.put("/home/crpier/Downloads/music/4.mp3")
temp_queue.put("/home/crpier/Downloads/music/5.mp3")


class AbstractStationRepository(ABC):
    pass


class ShoutWrapper:
    def __init__(
        self,
        host: str,
        port: int,
        password: str,
        name: str,
        id: str,
        genre: str,
        description: str,
        format: str = "mp3",
        user: str = "source",
    ) -> None:
        self.conn = shout.Shout()

        self.conn.host = host
        self.conn.port = port
        self.conn.password = password
        self.conn.name = name
        self.conn.mount = f"/{id}"
        self.conn.genre = genre
        self.conn.description = description
        self.conn.format = format
        self.conn.user = user

    def open(self):
        self.conn.open()

    def send(self, data: bytes):
        self.conn.send(data)

    def sync(self):
        self.conn.sync()

    @classmethod
    def from_station(cls, station: Station):
        return cls(
            host=station.broadcastServer.hostname,
            port=station.broadcastServer.port,
            password=station.broadcastServer.password,
            user=station.broadcastServer.user,
            id=station.id,
            name=station.name,
            genre=station.genre,
            description=station.description,
        )


class InMemoryStationRepository(AbstractStationRepository):
    def __init__(self) -> None:
        self._container: Dict[str, Tuple[Station, Thread, ShoutWrapper]] = {}

    def create(self, new_station: Station):
        if self._container.get(new_station.id) is not None:
            return StationAlreadyExists

        new_conn = ShoutWrapper.from_station(new_station)
        new_thread = Thread(
            target=self._play_function, args=[new_station, new_conn], daemon=True
        )
        self._container[new_station.id] = (new_station, new_thread, new_conn)

    def play(self, station_id):
        res = self._container.get(station_id)
        if res is None:
            raise StationDoesNotExist
        _, thread, _ = res
        thread.start()

    def _play_function(self, station: Station, conn: ShoutWrapper):
        conn.open()
        song_path = Path(temp_queue.get())
        with song_path.open("rb") as music_file:
            nbuf = music_file.read(station.bitrate)
            while True:
                buf = nbuf
                nbuf = music_file.read(station.bitrate)
                if len(buf) == 0:
                    break
                conn.send(buf)
                conn.sync()

    def _register_connection(self, station: Station):
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

    def get_all(self) -> List[Station]:
        return [station for (station, _, _) in self._container.values()]

    def get_stations_by_user_id(self, user_id: user_id):
        result: List[Tuple[str, Station]] = []
        for key in self._container.keys():
            if key.startswith(user_id):
                result.append((key, self._container.get(key)))  # type: ignore
        return result

    def get(self, station_id: station_id) -> Station:
        return self._container[station_id][0]

    def remove(self, station: Station):
        if self._container.get(station.id) is None:
            raise StationDoesNotExist
        del self._container[station.id]


class StationAlreadyExists(BaseException):
    pass


class StationDoesNotExist(BaseException):
    pass
