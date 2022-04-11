from app.models.domain_model import Song, song_id
from copy import deepcopy
from typing import Dict
from abc import ABC


class AbstractSongRepository(ABC):
    pass


class LocalDiskSongRepository(AbstractSongRepository):
    _container: Dict[song_id, Song] = {}

    def get_song(self, song_id: song_id) -> Song:
        song = self._container.get(song_id)
        if song is None:
            raise SongNotFound
        return deepcopy(song)

    def add_song(self, song: Song) -> Song:
        # Is this really convoluted actually? Should I go to sleep instead?
        try:
            self.get_song(song.id)
        except SongNotFound:
            self._container[song.id] = song
            return deepcopy(song)
        else:
            raise DuplicateSongId

    def delete_song(self, song_id):
        song_to_del = self._container.get(song_id)
        if song_to_del is None:
            raise SongNotFound
        del self._container[song_id]


class SongNotFound(Exception):
    pass


class DuplicateSongId(Exception):
    pass
