from app.services.station_uow import ThreadStationUnitOfWork
from app.models.domain_model import Station, station_id
from app.schemas.station import StationCreate
from typing import List

def create_station(create_in: StationCreate, uow: ThreadStationUnitOfWork):
    with uow:
        new_station = Station(**create_in.__dict__)
        uow.add_station(new_station)
        uow.run_station(new_station.id)
        return new_station

def delete_station(station_id: station_id, uow: ThreadStationUnitOfWork):
    with uow:
        uow.stations.remove(station_id)

def get_all_stations(uow: ThreadStationUnitOfWork) -> List[Station]:
    with uow:
        return uow.stations.get_all()
