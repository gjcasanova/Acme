import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from app.models import Position, Vehicle
from app.models.enums import ProviderName
from app.repositories.vehicle_repository import VehicleRepository


@dataclass(frozen=True)
class LastPosition:
    lat: float
    lng: float
    recorded_at: datetime
    provider: ProviderName


@dataclass(frozen=True)
class VehicleWithLastPosition:
    uuid: uuid.UUID
    plate: str
    name: str
    last_position: LastPosition | None


class VehicleService:
    def __init__(self, vehicle_repository: VehicleRepository) -> None:
        self._vehicle_repository = vehicle_repository

    def list_vehicles(self) -> list[VehicleWithLastPosition]:
        return [
            _to_vehicle_with_last_position(vehicle, position)
            for vehicle, position in self._vehicle_repository.list_with_last_position()
        ]


def _to_vehicle_with_last_position(
    vehicle: Vehicle, position: Position | None
) -> VehicleWithLastPosition:
    return VehicleWithLastPosition(
        uuid=vehicle.uuid,
        plate=vehicle.plate,
        name=vehicle.name,
        last_position=_to_last_position(position),
    )


def _to_last_position(position: Position | None) -> LastPosition | None:
    if position is None:
        return None
    return LastPosition(
        lat=position.lat,
        lng=position.lng,
        recorded_at=_as_utc(position.recorded_at),
        provider=position.provider,
    )


def _as_utc(value: datetime) -> datetime:
    # SQLite does not preserve timezone info: it stores UTC datetimes as naive.
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)
