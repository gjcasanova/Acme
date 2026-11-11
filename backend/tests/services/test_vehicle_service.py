from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models import Position, Vehicle
from app.models.enums import ProviderName
from app.repositories.vehicle_repository import VehicleRepository
from app.services.vehicle_service import VehicleService


def _service(db: Session) -> VehicleService:
    return VehicleService(VehicleRepository(db))


def _add_vehicle(db: Session, *, plate: str) -> Vehicle:
    vehicle = Vehicle(plate=plate, name=f"Vehicle {plate}")
    db.add(vehicle)
    db.commit()
    return vehicle


def _add_position(
    db: Session,
    *,
    vehicle: Vehicle,
    recorded_at: datetime,
    received_at: datetime,
    provider: ProviderName = ProviderName.alpha,
    lat: float = 0.0,
    lng: float = 0.0,
) -> None:
    db.add(
        Position(
            vehicle_id=vehicle.id,
            lat=lat,
            lng=lng,
            recorded_at=recorded_at,
            received_at=received_at,
            provider=provider,
        )
    )
    db.commit()


def test_list_vehicles_returns_all_ordered_by_plate(db_session: Session) -> None:
    _add_vehicle(db_session, plate="ZZZ000")
    _add_vehicle(db_session, plate="AAA111")
    _add_vehicle(db_session, plate="MMM222")

    vehicles = _service(db_session).list_vehicles()

    assert [vehicle.plate for vehicle in vehicles] == ["AAA111", "MMM222", "ZZZ000"]


def test_vehicle_without_positions_has_none_last_position(db_session: Session) -> None:
    _add_vehicle(db_session, plate="ABC123")

    [vehicle] = _service(db_session).list_vehicles()

    assert vehicle.plate == "ABC123"
    assert vehicle.last_position is None


def test_returns_position_with_greatest_recorded_at(db_session: Session) -> None:
    vehicle = _add_vehicle(db_session, plate="ABC123")
    newer = datetime(2026, 11, 12, 4, 0, 0, tzinfo=UTC)
    older = datetime(2026, 11, 12, 3, 0, 0, tzinfo=UTC)
    # Inserted out of order: the newest arrives first.
    _add_position(db_session, vehicle=vehicle, recorded_at=newer, received_at=newer)
    _add_position(db_session, vehicle=vehicle, recorded_at=older, received_at=older)

    [result] = _service(db_session).list_vehicles()

    assert result.last_position is not None
    assert result.last_position.recorded_at == newer


def test_tie_in_recorded_at_prefers_greatest_received_at(db_session: Session) -> None:
    vehicle = _add_vehicle(db_session, plate="ABC123")
    recorded = datetime(2026, 11, 12, 3, 0, 0, tzinfo=UTC)
    earlier_received = datetime(2026, 11, 12, 3, 0, 1, tzinfo=UTC)
    later_received = datetime(2026, 11, 12, 3, 0, 2, tzinfo=UTC)
    _add_position(
        db_session, vehicle=vehicle, recorded_at=recorded, received_at=earlier_received, lat=1.0
    )
    _add_position(
        db_session, vehicle=vehicle, recorded_at=recorded, received_at=later_received, lat=2.0
    )

    [result] = _service(db_session).list_vehicles()

    assert result.last_position is not None
    assert result.last_position.lat == 2.0


def test_position_from_any_provider_wins_by_recorded_at(db_session: Session) -> None:
    vehicle = _add_vehicle(db_session, plate="JKL012")
    alpha_recorded = datetime(2026, 11, 12, 3, 0, 0, tzinfo=UTC)
    beta_recorded = datetime(2026, 11, 12, 5, 0, 0, tzinfo=UTC)
    _add_position(
        db_session,
        vehicle=vehicle,
        recorded_at=alpha_recorded,
        received_at=alpha_recorded,
        provider=ProviderName.alpha,
    )
    _add_position(
        db_session,
        vehicle=vehicle,
        recorded_at=beta_recorded,
        received_at=beta_recorded,
        provider=ProviderName.beta,
    )

    [result] = _service(db_session).list_vehicles()

    assert result.last_position is not None
    assert result.last_position.recorded_at == beta_recorded
    assert result.last_position.provider == ProviderName.beta
