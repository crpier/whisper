from typing import List

from fastapi import APIRouter, Depends

from app.models.domain_model import station_id, Station
from app import schemas
from app.services import station_services, user_services
from app.services.station_uow import (
    ThreadedStationUnitOfWork,
    get_thread_station_uow,
)

from app.models.domain_model import User, user_id

router = APIRouter()


@router.get("/", response_model=List[schemas.Station])
def get_all_station(
    station_uow: ThreadedStationUnitOfWork = Depends(get_thread_station_uow),
    current_user: User = Depends(user_services.get_current_user),
) -> List[Station]:
    """
    Retrieve users.
    """
    stations = station_services.get_all_stations(station_uow)
    return stations


@router.put("/{station_id}/unpause")
def unpause_station(
    station_id: station_id,
    station_uow: ThreadedStationUnitOfWork = Depends(get_thread_station_uow),
    current_user: User = Depends(user_services.get_current_user),
) -> None:
    station_services.unpause_station(station_id, station_uow)

@router.put("/{station_id}/pause")
def pause_station(
    station_id: station_id,
    station_uow: ThreadedStationUnitOfWork = Depends(get_thread_station_uow),
    current_user: User = Depends(user_services.get_current_user),
) -> None:
    station_services.pause_station(station_id, station_uow)



@router.post("/", response_model=schemas.Station)
def create_station(
    station_in: schemas.StationCreate,
    station_uow: ThreadedStationUnitOfWork = Depends(get_thread_station_uow),
    current_user: User = Depends(user_services.get_current_user),
) -> Station:
    """
    Retrieve users.
    """
    new_station = station_services.create_station(station_in, station_uow)
    return new_station


@router.delete("/{station_id}")
def delete_station(
    station_id: station_id,
    station_uow: ThreadedStationUnitOfWork = Depends(get_thread_station_uow),
    current_user: User = Depends(user_services.get_current_user),
) -> None:
    """
    Retrieve users.
    """
    station_services.delete_station(station_id, station_uow)
