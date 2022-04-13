from typing import List, Any

from fastapi import APIRouter, Depends

from app.services.song_uow import get_in_memory_song_uow
from app.services.song_services import get_songs_from_query
from app.models.domain_model import User
from app.services import user_services

uow = get_in_memory_song_uow()

router = APIRouter()


@router.get("/")
def get_song_from_query(
    query: str,
    current_user: User = Depends(user_services.get_current_user),
):
    return get_songs_from_query(query, uow)
