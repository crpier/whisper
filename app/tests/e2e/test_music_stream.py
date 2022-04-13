import time
from typing import Dict

from threading import Thread
import pytest
import vlc
from fastapi.testclient import TestClient

from app.core.config import settings


def send_start_station_req(client: TestClient, headers, data):
    r = client.post(
        f"{settings.API_V1_STR}/station/",
        headers=headers,
        json=data,
    )
    assert r.status_code == 200


port = 8000
short_wait_for_connection_time = 1
broadcastServerHost = "icecast.crpier.xyz"
station_id = "tester"


@pytest.fixture
def station(client: TestClient, superuser_token_headers: Dict[str, str]):
    data = {
        "id": station_id,
        "name": "lolaw",
        "description": "string",
        "owner_id": "1",
        "genre": "rock",
        "bitrate": 1024,
        "broadcastServer": {
            "hostname": broadcastServerHost,
            "password": "mamatata1",
            "user": "source",
            "port": port,
        },
    }
    station_thread = Thread(
        target=send_start_station_req,
        args=(client, superuser_token_headers, data),
    )
    time.sleep(2)
    station_thread.run()
    url = f"http://{broadcastServerHost}:{port}/{station_id}"
    return url


@pytest.fixture
def player(station: str):
    instance = vlc.Instance()
    assert instance is not None

    player = instance.media_player_new()
    media = instance.media_new(station)

    player.set_media(media)
    return player


def test_station_works(player):
    player.play()
    # sleep ensures vlc had time to connect
    time.sleep(short_wait_for_connection_time)
    state = player.get_state()
    assert state == vlc.State.Playing  # type: ignore
