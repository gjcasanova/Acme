from datetime import UTC, datetime

from pydantic import BaseModel, Field

from app.adapters.base import NormalizedPosition
from app.models.enums import ProviderName


class BetaCoords(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class BetaPayload(BaseModel):
    unit_code: str = Field(min_length=1)
    coords: BetaCoords
    epoch: int = Field(gt=0)


class BetaAdapter:
    provider = ProviderName.beta

    def to_normalized(self, payload: BetaPayload) -> NormalizedPosition:
        return NormalizedPosition(
            external_id=payload.unit_code,
            provider=self.provider,
            lat=payload.coords.latitude,
            lng=payload.coords.longitude,
            recorded_at=datetime.fromtimestamp(payload.epoch, tz=UTC),
        )
