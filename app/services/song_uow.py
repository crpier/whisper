from typing import Generator, List
from app.adapters.song_repository import LocalDiskSongRepository
from app.models.domain_model import song_id, Song
from functools import lru_cache


class AbstractSongUow:
    pass


class InMemorySongUow(AbstractSongUow):
    repo: LocalDiskSongRepository = LocalDiskSongRepository()

    def __enter__(self):
        pass

    def __exit__(self, *_):
        pass

    def get_all_songs(self) -> List[Song]:
        return self.repo.get_all_songs()

    def register_song(self, song):
        self.repo.add_song(song)

    def get_song_data(self, song_id: song_id):
        return self.repo.get_song(song_id)

    def stream_song_generator(
        self, song_id: song_id, bitrate: int
    ) -> Generator[bytes, None, None]:
        song_data = self.repo.get_song(song_id)
        with open(song_data.source, "rb") as music_file:
            nbuf = music_file.read(bitrate)
            while True:
                buf = nbuf
                nbuf = music_file.read(bitrate)
                if len(buf) == 0:
                    break
                yield buf


@lru_cache
def get_in_memory_song_uow() -> InMemorySongUow:
    uow = InMemorySongUow()
    return uow
