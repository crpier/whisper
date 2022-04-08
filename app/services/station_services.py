from app.services.station_uow import ThreadStationUnitOfWork
from app.models.domain_model import Station, station_id
from app.schemas.station import StationCreate

def create_station(create_in: StationCreate, uow: ThreadStationUnitOfWork):
    with uow:
        new_station = Station(**create_in.__dict__)
        uow.add_station(new_station)
        uow.run_station(new_station.id)


def connect_to_station_server(station_id: station_id, uow: ThreadStationUnitOfWork):
    with uow:
        uow.connect_to_broadcast_server(station_id)
