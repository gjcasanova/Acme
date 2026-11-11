from datetime import UTC

from pydantic import AwareDatetime, BaseModel, Field

from app.adapters.base import NormalizedPosition
from app.models.enums import ProviderName


class AlphaPayload(BaseModel):
    vehicle_id: str = Field(min_length=1)
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    ts: AwareDatetime


class AlphaAdapter:
    provider = ProviderName.alpha

    def to_normalized(self, payload: AlphaPayload) -> NormalizedPosition:
        return NormalizedPosition(
            external_id=payload.vehicle_id,
            provider=self.provider,
            lat=payload.lat,
            lng=payload.lng,
            recorded_at=payload.ts.astimezone(UTC),
        )
