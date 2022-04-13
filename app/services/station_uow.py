from dataclasses import dataclass
from queue import Empty, Queue
from abc import ABC
from functools import lru_cache
from threading import Event, Thread
from typing import Any, List
from app.services.song_uow import InMemorySongUow
import shout

from app.adapters.station.repository import InMemoryStationRepository
from app.models.domain_model import Station, station_id, State, Song, song_id


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
    queue: Queue[Song]

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

    def clear_queue(self):
        cleared_count = 0
        while not self.queue.empty():
            try:
                self.queue.get()
                cleared_count += 1
            except Empty:
                pass
        return cleared_count

    def append_queue(self, song: Song):
        self.queue.put(song)


class ThreadedStationUnitOfWork(AbstractStationUnitOfWork):
    repo = InMemoryStationRepository[StationMeta]()
    song_uow = InMemorySongUow()

    def __enter__(self):
        pass

    def __exit__(self, *_):
        pass

    def create_station(self, new_station: Station):
        new_queue = Queue()
        new_queue.put(
            Song(
                title="test",
                album="test",
                artist="test",
                source="test_music/1.mp3",
                id=song_id("1.mp3"),
            )
        )
        new_queue.put(
            Song(
                title="test",
                album="test",
                artist="test",
                source="test_music/2.mp3",
                id=song_id("2.mp3"),
            )
        )
        new_queue.put(
            Song(
                title="test",
                album="test",
                artist="test",
                source="test_music/3.mp3",
                id=song_id("3.mp3"),
            )
        )
        new_queue.put(
            Song(
                title="test",
                album="test",
                artist="test",
                source="test_music/4.mp3",
                id=song_id("4.mp3"),
            )
        )
        new_events = StationEvents()
        new_conn = ShoutWrapper.from_station(new_station)
        new_thread = Thread(
            target=self._play_function,
            args=[new_station, new_conn, new_events, new_queue],
            daemon=True,
        )

        station_meta = StationMeta(
            thread=new_thread,
            conn=new_conn,
            events=new_events,
            queue=new_queue,
        )
        station_meta.set_event("play")
        aggregate = (new_station, station_meta)
        self.repo.add(aggregate)

    def _play_function(
        self,
        station: Station,
        conn: ShoutWrapper,
        events: StationEvents,
        queue: Queue[Song],
    ):
        conn.open()
        while True:
            song = queue.get()
            stream_generator = self.song_uow.stream_song_generator(
                song.id, station.bitrate
            )
            for buf in stream_generator:
                if not events.stop.is_set() and events.play.wait():
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

    def get_next_songs(self, station_id: station_id) -> List[Any]:
        station_meta = self.repo.get_meta(station_id)
        queue_as_list = list(station_meta.queue.queue)
        return queue_as_list

    def clear_queue(self, station_id: station_id) -> int:
        station_meta = self.repo.get_meta(station_id)
        return station_meta.clear_queue()

    def append_queue(self, station_id: station_id, song_id: song_id):
        station_meta = self.repo.get_meta(station_id)
        song = self.song_uow.get_song_data(song_id)
        return station_meta.append_queue(song)


@lru_cache
def get_thread_station_uow():
    return ThreadedStationUnitOfWork()
