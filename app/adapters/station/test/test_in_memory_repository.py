from pytest import fixture, mark

from mock import MagicMock
from app.models.domain_model import (
    BroadcastServer,
    Station,
    station_id,
    user_id,
)


@fixture
def station() -> Station:
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
