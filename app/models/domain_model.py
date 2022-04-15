from dataclasses import dataclass
from typing import List, NewType, Optional

from pydantic.networks import EmailStr
from enum import Enum

user_id = NewType("user_id", str)
station_id = NewType("station_id", str)
playlist_id = NewType("playlist_id", str)
song_id = NewType("song_id", str)


@dataclass(frozen=True)
class Song:
    id: song_id
    title: str
    album: str
    artist: str
    source: str


@dataclass(frozen=True)
class Playlist:
    id: playlist_id
    songs: List[Song]
    public: bool
    owner_id: user_id


@dataclass(frozen=True)
class BroadcastServer:
    hostname: str
    password: str
    user: str
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
    ) -> None:
        self.id = id
        self.owner_id = owner_id
        self.genre = genre
        self.name = name
        self.description = description
        self.broadcastServer = broadcastServer
        self.bitrate = bitrate

        self.state: State = State.STOPPED
        self.running = False

    def set_state(self, state: State):
        self.state = state

    @property
    def station_url(self):
        url = f"http://{self.broadcastServer.hostname}:{self.broadcastServer.port}/{self.id}"
        return url


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
