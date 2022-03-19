from app.models.domain_model import *


def get_test_song():
    return NotImplementedError


def get_playlist_and_songs():
    return NotImplementedError


def get_test_queue():
    return NotImplementedError


def get_test_station():
    return NotImplementedError


def get_test_playlist():
    return NotImplementedError


def test_queue_from_playlist_has_same_songs():
    _, test_playlist = get_playlist_and_songs()
    test_queue = StationQueue.from_playlist(test_playlist)
    assert test_queue.queue_list == test_playlist.songs


def test_station_queue_is_empty_after_clear():
    queue: StationQueue = get_test_queue()
    queue.clear()
    assert queue.queue_list == []
    assert queue.current_song == None


def test_queue_append_adds_song_at_end():
    queue: StationQueue = get_test_queue
    song = get_test_song()
    expected_queue_list = queue.queue_list.append(song)

    queue.append(song)
    assert queue.queue_list == expected_queue_list


def test_station_after_start_streaming_is_running():
    station: Station = get_test_station()
    playlist = get_test_playlist()
    station.start_streaming(playlist)
    assert station.running == True
