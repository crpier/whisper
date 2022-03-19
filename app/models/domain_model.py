from typing import List, NewType, Optional
from dataclasses import dataclass
from queue import Queue

user_id = NewType(str)
station_id = NewType(str)
playlist_id = NewType(str)

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
    _queue: Queue

    @property
    def current_song() -> Optional[Song]:
        return NotImplementedError

    @property
    def queue_list(self):
        return list(self._queue)

    @classmethod
    def from_playlist(cls, playlist: Playlist):
        print(playlist)
        return NotImplementedError

    def append(song: Song):
        return NotImplementedError

    def clear():
        return NotImplementedError

    def update_next_songs(songs: List[Song]):
        return NotImplementedError


class Station:
    id: station_id
    name: str
    status: str
    queue: StationQueue

    def start_streaming(self, playlist: Playlist):
        self.queue = StationQueue.from_playlist(playlist)
        self.running = True
        return NotImplementedError

    def pause_streaming(self):
        return NotImplementedError

    def unpause_streaming(self):
        return NotImplementedError

    def get_status(self):
        return NotImplementedError


class User:
    id: user_id
    name: str
    email: str
    stations: List[Station]
    own_playlists: List[Playlist]
    saved_playlists: List[Playlist]

    def create_playlist(self, playlist: Playlist):
        print(playlist)
        return NotImplementedError

    def update_playlist(self, playlist_id: playlist_id):
        print(playlist_id)
        return NotImplementedError

    def delete_playlist(self, playlist_id: playlist_id):
        print(playlist_id)
        return NotImplementedError

    def get_playlist(self, playlist_id: playlist_id):
        print(playlist_id)
        return NotImplementedError

    def share_playlist(self, playlist_id: playlist_id):
        print(playlist_id)
        return NotImplementedError

    def get_playlists(self):
        return NotImplementedError

    def create_station(self):
        return NotImplementedError

    def delete_station(self):
        return NotImplementedError

    def get_station(self):
        return NotImplementedError
