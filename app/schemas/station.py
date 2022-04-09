from typing import Optional

from pydantic import BaseModel

from app.models.domain_model import user_id, station_id


class BroadcastServerBase(BaseModel):
    hostname: Optional[str] = None
    password: Optional[str] = None
    user: Optional[str] = None
    port: Optional[int] = None


# Shared properties
class StationBase(BaseModel):
    id: Optional[station_id] = None
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[user_id] = None
    genre: Optional[str] = None
    bitrate: Optional[int] = None
    broadcastServer: Optional[BroadcastServerBase] = None


# Properties to receive on item creation
class StationCreate(StationBase):
    id: station_id
    description: str
    owner_id: user_id
    genre: str
    bitrate: int
    broadcastServer: BroadcastServerBase


# Properties to receive on item update
class StationUpdate(StationBase):
    pass


class StationInDBBase(StationBase):
    class Config:
        orm_mode = True


class Station(StationInDBBase):
    pass


class StationInDB(StationInDBBase):
    pass
