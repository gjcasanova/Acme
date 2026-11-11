from datetime import UTC, datetime

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapters.alpha import AlphaPayload
from app.adapters.beta import BetaPayload
from app.models import Position, Vehicle
from app.models.enums import ProviderName
from app.repositories.position_repository import PositionRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.services.exceptions import VehicleNotFoundError
from app.services.position_service import PositionService


def _service(db: Session) -> PositionService:
    return PositionService(VehicleRepository(db), PositionRepository(db))


def _add_vehicle(
    db: Session,
    *,
    plate: str,
    alpha_id: str | None = None,
    beta_code: str | None = None,
) -> Vehicle:
    vehicle = Vehicle(plate=plate, name="Test vehicle", alpha_id=alpha_id, beta_code=beta_code)
    db.add(vehicle)
    db.commit()
    return vehicle


def test_register_from_alpha_stores_position_linked_to_vehicle(db_session: Session) -> None:
    vehicle = _add_vehicle(db_session, plate="ABC123", alpha_id="ALP-001")
    payload = AlphaPayload(
        vehicle_id="ALP-001", lat=4.6097, lng=-74.0817, ts="2026-11-12T03:15:00Z"
    )

    position = _service(db_session).register_from_alpha(payload)

    assert position.id is not None
    assert position.vehicle_id == vehicle.id
    assert position.provider == ProviderName.alpha
    assert position.lat == 4.6097
    assert position.lng == -74.0817
    assert position.recorded_at == datetime(2026, 11, 12, 3, 15, 0, tzinfo=UTC)

    stored = db_session.scalar(select(Position).where(Position.uuid == position.uuid))
    assert stored is not None
    assert stored.vehicle_id == vehicle.id
    assert stored.provider == ProviderName.alpha


def test_register_from_alpha_converts_ts_to_utc(db_session: Session) -> None:
    _add_vehicle(db_session, plate="ABC123", alpha_id="ALP-001")
    payload = AlphaPayload(
        vehicle_id="ALP-001", lat=1.0, lng=2.0, ts="2026-11-12T03:15:00-05:00"
    )

    position = _service(db_session).register_from_alpha(payload)

    assert position.recorded_at == datetime(2026, 11, 12, 8, 15, 0, tzinfo=UTC)


def test_register_from_alpha_assigns_received_at(db_session: Session) -> None:
    _add_vehicle(db_session, plate="ABC123", alpha_id="ALP-001")
    payload = AlphaPayload(vehicle_id="ALP-001", lat=1.0, lng=2.0, ts="2026-11-12T03:15:00Z")

    position = _service(db_session).register_from_alpha(payload)

    assert position.received_at is not None
    assert position.received_at.tzinfo is not None


def test_register_from_alpha_unknown_vehicle_raises(db_session: Session) -> None:
    _add_vehicle(db_session, plate="ABC123", alpha_id="ALP-001")
    payload = AlphaPayload(vehicle_id="UNKNOWN", lat=1.0, lng=2.0, ts="2026-11-12T03:15:00Z")

    with pytest.raises(VehicleNotFoundError):
        _service(db_session).register_from_alpha(payload)


def test_register_from_alpha_does_not_match_beta_code(db_session: Session) -> None:
    _add_vehicle(db_session, plate="GHI789", beta_code="BT-9001")
    payload = AlphaPayload(vehicle_id="BT-9001", lat=1.0, lng=2.0, ts="2026-11-12T03:15:00Z")

    with pytest.raises(VehicleNotFoundError):
        _service(db_session).register_from_alpha(payload)
