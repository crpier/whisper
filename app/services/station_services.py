from app.services.station_uow import ThreadedStationUnitOfWork
from app.models.domain_model import Station, station_id, song_id
from app import schemas
from typing import List


def create_station(
    create_in: schemas.station.StationCreate, uow: ThreadedStationUnitOfWork
) -> Station:
    with uow:
        new_station = Station(**create_in.__dict__)
        uow.create_station(new_station)
        uow.play_station(new_station.id)
        return new_station


def delete_station(station_id: station_id, uow: ThreadedStationUnitOfWork):
    with uow:
        uow.remove_station(station_id)


def get_all_stations(uow: ThreadedStationUnitOfWork) -> List[Station]:
    with uow:
        return uow.repo.get_all_stations()


def unpause_station(station_id: station_id, uow: ThreadedStationUnitOfWork):
    with uow:
        return uow.unpause_station(station_id)


def pause_station(station_id: station_id, uow: ThreadedStationUnitOfWork):
    with uow:
        return uow.pause_station(station_id)


# Queue stuff
def get_next_songs(station_id: station_id, uow: ThreadedStationUnitOfWork):
    with uow:
        return uow.get_next_songs(station_id)

def clear_queue(station_id: station_id, uow: ThreadedStationUnitOfWork) -> int:
    with uow:
        return uow.clear_queue(station_id)

def append_queue(station_id: station_id, song_id: song_id, uow: ThreadedStationUnitOfWork):
    with uow:
        return uow.append_queue(station_id, song_id)
