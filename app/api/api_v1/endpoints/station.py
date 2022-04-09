from typing import Any, List

from fastapi import APIRouter, Depends

from app.models.domain_model import station_id, Station
from app import schemas
from app.services import station_services
from app.services.station_uow import (
    ThreadStationUnitOfWork,
    get_thread_station_uow,
)


router = APIRouter()


@router.get("/", response_model=List[schemas.Station])
def get_all_station(
    station_uow: ThreadStationUnitOfWork = Depends(get_thread_station_uow),
) -> List[Station]:
    """
    Retrieve users.
    """
    stations = station_services.get_all_stations(station_uow)
    return stations

# @router.put("/{station_id}/pause"):
# def create_station(
#     station_in: schemas.StationCreate,
#     station_uow: ThreadStationUnitOfWork = Depends(get_thread_station_uow),
# ) -> Any:


@router.post("/", response_model=schemas.Station)
def create_station(
    station_in: schemas.StationCreate,
    station_uow: ThreadStationUnitOfWork = Depends(get_thread_station_uow),
) -> Station:
    """
    Retrieve users.
    """
    new_station = station_services.create_station(station_in, station_uow)
    # TODO: figure out why we need to turn this to dict
    return new_station


@router.delete("/{station_id}")
def delete_station(
    station_id: station_id,
    station_uow: ThreadStationUnitOfWork = Depends(get_thread_station_uow),
) -> None:
    """
    Retrieve users.
    """
    station_services.delete_station(station_id, station_uow)
