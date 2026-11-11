from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.models.enums import ProviderName


@dataclass(frozen=True)
class NormalizedPosition:
    external_id: str
    provider: ProviderName
    lat: float
    lng: float
    recorded_at: datetime


class ProviderAdapter(Protocol):
    provider: ProviderName

    def to_normalized(self, payload: object) -> NormalizedPosition: ...
