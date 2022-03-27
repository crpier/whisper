from dataclasses import dataclass
from queue import Queue
from typing import List, NewType, Optional

from app.core.security import get_password_hash

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
    def __init__(self, playlist: Playlist | None = None) -> None:
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

    def append(self, song: Song):
        self._queue.put(song)

    def clear(self):
        while not self._queue.empty():
            self._queue.get()

    def update_next_songs(self, songs: List[Song]):
        print(songs)
        raise NotImplementedError


class Station:
    def __init__(
        self,
        id: station_id,
        name: str,
        owner_id: user_id,
        playlist: Playlist | None = None,
    ) -> None:
        self.id = id
        self.owner_id = owner_id
        self.name = name
        self.status = "Stopped"
        self.running = False
        self.queue = StationQueue(playlist)

    def start_streaming(self):
        raise NotImplementedError

    def pause_streaming(self):
        raise NotImplementedError

    def unpause_streaming(self):
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError


class User:
    def __init__(
        self, id: user_id, name: str, email: str, password: str
    ) -> None:
        self.id: user_id = id
        self.name: str = name
        self.email: str = email
        self.hashed_password = password
        self.stations: List[Station] = []
        self.own_playlists: List[Playlist] = []
        self.saved_playlists: List[Playlist] = []

    def create_playlist(self, playlist: Playlist):
        print(playlist)
        raise NotImplementedError

    def update_playlist(self, playlist_id: playlist_id):
        print(playlist_id)
        raise NotImplementedError

    def delete_playlist(self, playlist_id: playlist_id):
        print(playlist_id)
        raise NotImplementedError

    def get_playlist(self, playlist_id: playlist_id):
        print(playlist_id)
        raise NotImplementedError

    def share_playlist(self, playlist_id: playlist_id):
        print(playlist_id)
        raise NotImplementedError

    def get_playlists(self):
        raise NotImplementedError

    def create_station(self):
        raise NotImplementedError

    def delete_station(self):
        raise NotImplementedError

    def get_station(self):
        raise NotImplementedError
