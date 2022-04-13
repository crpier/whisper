import logging

from app.core.config import settings
from app.models.domain_model import Song, song_id
from app.schemas.user import UserCreate  # noqa: F401
from app.services import user_services
from app.services.song_uow import get_in_memory_song_uow
from app.services.user_uow import get_sqlalchemy_uow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    user_in = UserCreate(
        email=settings.FIRST_SUPERUSER_EMAIL,
        name=settings.FIRST_SUPERUSER_NAME,
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )
    try:
        user_services.create_user(create_obj=user_in, uow=get_sqlalchemy_uow())
    except user_services.DuplicateException:
        pass


def make_song(file_name: str):
    return Song(
        title="name",
        album="test",
        artist="test",
        source=f"{settings.SONGS_PATH}/{file_name}",
        id=song_id(file_name),
    )


def init_in_memory_songs():
    new_uow = get_in_memory_song_uow()
    new_uow.register_song(make_song("1.mp3"))
    new_uow.register_song(make_song("2.mp3"))
    new_uow.register_song(make_song("3.mp3"))
    new_uow.register_song(make_song("4.mp3"))


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
