from typing import List
from app.models.domain_model import Song
from app.services.song_uow import InMemorySongUow


def get_songs_from_query(query: str, uow: InMemorySongUow) -> List[Song]:
    # TODO: lmao nice
    with uow:
        return uow.get_all_songs()
