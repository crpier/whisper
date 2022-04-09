from typing import Any

from pytest import fixture, mark

from app.models.domain_model import *


def get_test_song(name_part: Any):
    new_song = Song(
        title=f"test_title_{name_part}",
        album=f"test_album_{name_part}",
        artist=f"test_artist_{name_part}",
    )
    return new_song


@fixture
def base_song():
    new_song = Song(
        title="test_title", album="test_album", artist="test_artist"
    )
    return new_song


@fixture
def empty_queue():
    new_queue = StationQueue()
    return new_queue


@fixture
def one_song_queue():
    new_queue = StationQueue()
    new_queue.add_song(get_test_song(1))
    return new_queue


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
        playlist=get_test_playlist(),
        broadcastServer=BroadcastServer(
            hostname="test",
            user="test",
            password="test_pass",
            port=1234
        )
    )
    return new_station


def test_queue_append_adds_song_at_end(empty_queue, base_song):
    expected_queue_list = [base_song]
    empty_queue.add_song(base_song)
    assert empty_queue.queue_list == expected_queue_list


def test_queue_from_playlist_has_same_songs(three_song_playlist):
    test_queue = StationQueue(three_song_playlist)
    assert test_queue.queue_list == three_song_playlist.songs


def test_station_queue_is_empty_after_clear(one_song_queue):
    one_song_queue.clear()
    assert one_song_queue.queue_list == []
    assert one_song_queue.current_song == None


def test_current_queue_song_is_correct(one_song_queue):
    current_song = one_song_queue.current_song
    assert current_song is not None
    expected_song = one_song_queue._queue.get()
    assert expected_song == current_song


@mark.skip("Not Implemented")
def test_station_after_start_streaming_is_running(station_with_playlist):
    station_with_playlist.start_streaming()
    assert station_with_playlist.running == True
