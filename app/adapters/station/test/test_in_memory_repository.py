from pytest import fixture, mark

from mock import MagicMock
from app.models.domain_model import (
    BroadcastServer,
    Station,
    station_id,
    user_id,
)
from app.adapters.station.repository import (
    InMemoryStationRepository,
    ShoutWrapper,
)

@fixture
def test_station() -> Station:
    station = Station(
        id=station_id("test_station"),
        name="testing",
        description="station for test",
        owner_id=user_id("1"),
        genre="rock",
        bitrate=2048,
        broadcastServer=BroadcastServer(
            hostname="icecast.crpier.xyz",
            password="mamatata1",
            user="source",
            port=8000,
        ),
    )
    return station


@fixture
def test_conn(test_station) -> ShoutWrapper:
    conn = ShoutWrapper.from_station(test_station)
    return conn


@fixture
def test_repo():
    return InMemoryStationRepository()


@mark.component
def test_play_function_uses_shout_connection(
    test_station: Station,
    test_repo: InMemoryStationRepository,
):
    test_conn = MagicMock()
    test_conn.open = MagicMock()
    test_conn.send = MagicMock()
    test_conn.sync = MagicMock()
    test_repo._play_function(test_station, test_conn)
    test_conn.open.assert_called_once()
    test_conn.sync.assert_called()
    test_conn.send.assert_called()
