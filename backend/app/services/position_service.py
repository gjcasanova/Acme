from datetime import UTC, datetime

from app.adapters.alpha import AlphaAdapter, AlphaPayload
from app.adapters.base import NormalizedPosition
from app.adapters.beta import BetaAdapter, BetaPayload
from app.models import Position
from app.repositories.position_repository import PositionRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.services.exceptions import VehicleNotFoundError


class PositionService:
    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        position_repository: PositionRepository,
    ) -> None:
        self._vehicle_repository = vehicle_repository
        self._position_repository = position_repository

    def register_from_alpha(self, payload: AlphaPayload) -> Position:
        return self._register(AlphaAdapter().to_normalized(payload))

    def _register(self, normalized: NormalizedPosition) -> Position:
        vehicle = self._vehicle_repository.get_by_external_id(
            normalized.provider, normalized.external_id
        )
        if vehicle is None:
            raise VehicleNotFoundError(normalized.provider)
        position = Position(
            vehicle_id=vehicle.id,
            lat=normalized.lat,
            lng=normalized.lng,
            recorded_at=normalized.recorded_at,
            received_at=datetime.now(UTC),
            provider=normalized.provider,
        )
        position.vehicle = vehicle
        return self._position_repository.add(position)
