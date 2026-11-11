import uuid
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.api.dependencies import get_vehicle_service
from app.main import app
from app.models.enums import ProviderName
from app.services.vehicle_service import LastPosition, VehicleWithLastPosition


class _FakeVehicleService:
    def __init__(self, vehicles: list[VehicleWithLastPosition]) -> None:
        self._vehicles = vehicles

    def list_vehicles(self) -> list[VehicleWithLastPosition]:
        return self._vehicles


def _vehicle(*, last_position: LastPosition | None) -> VehicleWithLastPosition:
    return VehicleWithLastPosition(
        uuid=uuid.UUID("12345678-1234-5678-1234-567812345678"),
        plate="ABC123",
        name="Camión 01",
        last_position=last_position,
    )


def test_list_vehicles_returns_200_with_expected_shape(client: TestClient) -> None:
    last_position = LastPosition(
        lat=4.6097,
        lng=-74.0817,
        recorded_at=datetime(2026, 11, 12, 3, 15, 0, tzinfo=UTC),
        provider=ProviderName.alpha,
    )
    app.dependency_overrides[get_vehicle_service] = lambda: _FakeVehicleService(
        [_vehicle(last_position=last_position), _vehicle(last_position=None)]
    )
    try:
        response = client.get("/vehicles")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body == [
        {
            "uuid": "12345678-1234-5678-1234-567812345678",
            "plate": "ABC123",
            "name": "Camión 01",
            "last_position": {
                "lat": 4.6097,
                "lng": -74.0817,
                "recorded_at": "2026-11-12T03:15:00Z",
                "provider": "alpha",
            },
        },
        {
            "uuid": "12345678-1234-5678-1234-567812345678",
            "plate": "ABC123",
            "name": "Camión 01",
            "last_position": None,
        },
    ]


def test_list_vehicles_requires_no_authorization(client: TestClient) -> None:
    app.dependency_overrides[get_vehicle_service] = lambda: _FakeVehicleService([])
    try:
        response = client.get("/vehicles")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == []
