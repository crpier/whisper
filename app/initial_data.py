import logging

from app.core.config import settings
from app.models.domain_model import Song, song_id
from app.schemas.user import UserCreate  # noqa: F401
from app.services import user_services
from app.services.song_uow import InMemorySongUow
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


def init_in_memory_songs():
    new_uow = InMemorySongUow()

    new_uow.register_song(
        Song(
            title="test",
            album="test",
            artist="test",
            source="test_music/1.mp3",
            id=song_id("test1"),
        )
    )
    new_uow.register_song(
        Song(
            title="test",
            album="test",
            artist="test",
            source="test_music/2.mp3",
            id=song_id("test2"),
        )
    )
    new_uow.register_song(
        Song(
            title="test",
            album="test",
            artist="test",
            source="test_music/3.mp3",
            id=song_id("test3"),
        )
    )
    new_uow.register_song(
        Song(
            title="test",
            album="test",
            artist="test",
            source="test_music/4.mp3",
            id=song_id("test4"),
        )
    )


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
