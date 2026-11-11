import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import ProviderName


class PositionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: uuid.UUID
    vehicle_uuid: uuid.UUID
    lat: float
    lng: float
    recorded_at: datetime
    received_at: datetime
    provider: ProviderName
