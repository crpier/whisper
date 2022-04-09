from dataclasses import dataclass
from queue import Queue
from abc import ABC
from functools import lru_cache
from pathlib import Path
from threading import Event, Thread
from typing import Dict, Type, List

import shout

from app.adapters.station.repository import InMemoryStationRepository
from app.models.domain_model import Station, station_id, State


class AbstractStationUnitOfWork(ABC):
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

    def close(self):
        self.conn.close()

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


temp_queue = Queue()
temp_queue.put("test_music/1.mp3")
temp_queue.put("test_music/2.mp3")
temp_queue.put("test_music/3.mp3")
temp_queue.put("test_music/4.mp3")
temp_queue.put("test_music/5.mp3")


@dataclass
class StationEvents:
    def __init__(self) -> None:
        self.stop = Event()
        self.play = Event()


@dataclass
class StationMeta:
    thread: Thread
    conn: ShoutWrapper
    events: StationEvents

    def set_event(self, event_name: str):
        event: Event = getattr(self.events, event_name)
        event.set()

    def clear_event(self, event_name: str):
        event: Event = getattr(self.events, event_name)
        event.clear()

    def start_thread(self):
        self.thread.start()

    def close_connection(self):
        self.conn.close()


class ThreadedStationUnitOfWork(AbstractStationUnitOfWork):
    repo = InMemoryStationRepository[StationMeta]()

    def __enter__(self):
        pass

    def __exit__(self, *_):
        pass

    def create_station(self, new_station: Station):
        new_events = StationEvents()
        new_conn = ShoutWrapper.from_station(new_station)
        new_thread = Thread(
            target=self._play_function,
            args=[new_station, new_conn, new_events],
            daemon=True,
        )
        station_meta = StationMeta(
            thread=new_thread, conn=new_conn, events=new_events
        )
        station_meta.set_event("play")
        aggregate = (new_station, station_meta)
        self.repo.add(aggregate)

    def _play_function(
        self, station: Station, conn: ShoutWrapper, events: StationEvents
    ):
        conn.open()
        song_path = Path(temp_queue.get())
        with song_path.open("rb") as music_file:
            nbuf = music_file.read(station.bitrate)
            while not events.stop.is_set() and events.play.wait():
                buf = nbuf
                nbuf = music_file.read(station.bitrate)
                if len(buf) == 0:
                    break
                conn.send(buf)
                conn.sync()

    def remove_station(self, station_id: station_id):
        self.stop_station(station_id)
        self.repo.remove(station_id)

    def pause_station(self, station_id):
        station, meta = self.repo.get(station_id)
        meta.clear_event("play")
        station.set_state(State.PAUSED)

    def unpause_station(self, station_id):
        station, meta = self.repo.get(station_id)
        meta.set_event("play")
        station.set_state(State.PLAYING)

    def play_station(self, station_id: station_id) -> None:
        station, stationMeta = self.repo.get(station_id)
        stationMeta.start_thread()
        station.set_state(State.PLAYING)

    def stop_station(self, station_id: station_id) -> None:
        stationMeta = self.repo.get_meta(station_id)
        stationMeta.set_event("stop")
        stationMeta.close_connection()


@lru_cache
def get_thread_station_uow():
    return ThreadedStationUnitOfWork()
