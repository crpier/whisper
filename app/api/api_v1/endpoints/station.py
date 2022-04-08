from typing import Any, List

from fastapi import APIRouter, Depends

from app import schemas
from app.services import station_services
from app.services.station_uow import ThreadStationUnitOfWork, get_thread_station_uow



router = APIRouter()

@router.post("/", response_model=schemas.Station)
def create_station(
    station_in: schemas.StationCreate, 
    station_uow: ThreadStationUnitOfWork = Depends(get_thread_station_uow),
) -> Any:
    """
    Retrieve users.
    """
    users = station_services.create_station(station_in, station_uow)
    return users
