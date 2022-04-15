from typing import Any

from pytest import fixture, mark

from app.models.domain_model import *


def get_test_song(name_part: Any):
    new_song = Song(
        title=f"test_title_{name_part}",
        album=f"test_album_{name_part}",
        artist=f"test_artist_{name_part}",
        id=song_id(f"test_id_{name_part}"),
        source=f"/test/source/{name_part}",
    )
    return new_song


@fixture
def base_song():
    new_song = Song(
        title="test_title",
        album="test_album",
        artist="test_artist",
        id=song_id("test_id"),
        source="/test/source",
    )
    return new_song


def get_test_playlist():
    songs = [get_test_song(1), get_test_song(2), get_test_song(3)]
    new_playlist = Playlist(
        id=playlist_id("test"),
        songs=songs,
        public=True,
        owner_id=user_id("test"),
    )
    return new_playlist


@fixture
def three_song_playlist():
    return get_test_playlist()


@fixture
def station_with_playlist():
    new_station = Station(
        id=station_id("test"),
        description="Test description",
        owner_id=user_id("123"),
        genre="test genre",
        bitrate=1024,
        name="test",
        broadcastServer=BroadcastServer(
            hostname="test", user="test", password="test_pass", port=1234
        ),
    )
    return new_station


@mark.skip("Not Implemented")
@mark.unit
def test_station_after_start_streaming_is_running(station_with_playlist):
    station_with_playlist.start_streaming()
    assert station_with_playlist.running == True
