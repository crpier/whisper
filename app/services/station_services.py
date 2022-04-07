from app.services.station_uow import ThreadStationUnitOfWork
from app.models.domain_model import Station

def connect_to_station_server(station: Station, uow: ThreadStationUnitOfWork):
    with uow:
        uow.connect_to_broadcast_server(station)
