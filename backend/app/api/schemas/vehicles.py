import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import ProviderName


class LastPositionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lat: float
    lng: float
    recorded_at: datetime
    provider: ProviderName


class VehicleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: uuid.UUID
    plate: str
    name: str
    last_position: LastPositionOut | None
