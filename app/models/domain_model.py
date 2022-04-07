from dataclasses import dataclass
from queue import Queue
from typing import List, NewType, Optional

from pydantic.networks import EmailStr
from sqlalchemy.sql.sqltypes import Enum

user_id = NewType("user_id", str)
station_id = NewType("station_id", str)
playlist_id = NewType("playlist_id", str)


@dataclass(frozen=True)
class Song:
    title: str
    album: str
    artist: str


@dataclass(frozen=True)
class Playlist:
    id: playlist_id
    songs: List[Song]
    public: bool
    owner_id: user_id


class StationQueue:
    def __init__(self, playlist: Optional[Playlist] = None) -> None:
        new_queue = Queue()
        if playlist:
            for song in playlist.songs:
                new_queue.put(song)
        self._queue = new_queue

    @property
    def current_song(self) -> Optional[Song]:
        try:
            return self._queue.queue[0]
        except IndexError:
            return None

    @property
    def queue_list(self):
        return list(self._queue.queue)

    def add_song(self, song: Song):
        self._queue.put(song)

    def clear(self):
        while not self._queue.empty():
            self._queue.get()

@dataclass
class BroadcastServer:
    hostname: str
    password: str
    user: str
    # TODO: is there really no validator for port?
    port: int


class Station:
    def __init__(
        self,
        id: station_id,
        name: str,
        description: str,
        owner_id: user_id,
        genre: str,
        broadcastServer: BroadcastServer,
        bitrate: int,
        playlist: Optional[Playlist] = None,
    ) -> None:
        self.id = id
        self.owner_id = owner_id
        self.genre = genre
        self.name = name
        self.description = description
        self.broadcastServer = broadcastServer
        self.bitrate = bitrate

        self.queue = StationQueue(playlist)

        self.status = "Stopped"
        self.running = False

    def start_streaming(self):
        raise NotImplementedError

    def pause_streaming(self):
        raise NotImplementedError

    def resume_streaming(self):
        raise NotImplementedError

    def get_current_song(self):
        raise NotImplementedError


@dataclass
class Tier:
    max_stations: int
    max_created_playlists: int
    max_saved_playlists: int


class Tiers(Enum):
    FREE = Tier(
        max_stations=0,
        max_created_playlists=0,
        max_saved_playlists=0,
    )
    BASIC = Tier(
        max_stations=1,
        max_created_playlists=1,
        max_saved_playlists=3,
    )
    PREMIUM = Tier(
        max_stations=3,
        max_created_playlists=3,
        max_saved_playlists=10,
    )
    ADMIN = Tier(
        max_stations=99,
        max_created_playlists=99,
        max_saved_playlists=99,
    )


class User:
    def __init__(
        self,
        name: str,
        email: EmailStr,
        hashed_password: str,
        tier: Optional[Tier] = Tiers.FREE,
        id: Optional[user_id] = None,
    ) -> None:
        self.name: str = name
        self.email: str = email
        self.hashed_password = hashed_password
        self.stations: List[Station] = []
        self.own_playlists: List[Playlist] = []
        self.saved_playlists: List[Playlist] = []
        self.tier = tier
        if id:
            self.id: user_id
