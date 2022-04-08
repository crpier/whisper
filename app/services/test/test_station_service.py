from pytest import fixture, mark
import time

from app.models.domain_model import BroadcastServer, Station, station_id, user_id
from app.schemas.station import StationCreate
from app.services.station_services import create_station
from app.services.station_uow import ThreadStationUnitOfWork

@fixture
def station_in() -> StationCreate:
    station = StationCreate(
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
        )
    )
    return station

@mark.component
def test_create_station_works(station_in):
    uow = ThreadStationUnitOfWork()
    create_station(station_in, uow)
    time.sleep(100)
