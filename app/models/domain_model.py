from dataclasses import dataclass
from queue import Queue
from typing import List, NewType, Optional

from pydantic.networks import EmailStr
from enum import Enum

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


@dataclass(frozen=True)
class BroadcastServer:
    hostname: str
    password: str
    user: str
    # TODO: is there really no validator for port?
    port: int


class State(Enum):
    PAUSED = "paused"
    PLAYING = "playing"
    STOPPED = "stopped"


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

        self.state: State = State.STOPPED
        self.running = False

    def set_state(self, state: State):
        self.state = state

@dataclass(frozen=True)
class TierType:
    max_stations: int
    max_private_stations: int
    max_created_playlists: int
    max_saved_playlists: int


class Tier(Enum):
    FREE = TierType(
        max_stations=0,
        max_private_stations=0,
        max_created_playlists=0,
        max_saved_playlists=0,
    )
    BASIC = TierType(
        max_stations=1,
        max_private_stations=0,
        max_created_playlists=1,
        max_saved_playlists=3,
    )
    PREMIUM = TierType(
        max_stations=3,
        max_private_stations=1,
        max_created_playlists=3,
        max_saved_playlists=10,
    )
    ADMIN = TierType(
        max_stations=99,
        max_private_stations=99,
        max_created_playlists=99,
        max_saved_playlists=99,
    )


class User:
    def __init__(
        self,
        name: str,
        email: EmailStr,
        hashed_password: str,
        tier: Tier = Tier.FREE,
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
