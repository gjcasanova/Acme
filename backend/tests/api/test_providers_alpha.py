import uuid
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.adapters.alpha import AlphaPayload
from app.api.dependencies import get_auth_service, get_position_service
from app.main import app
from app.models import Position, Vehicle
from app.models.enums import ProviderName
from app.services.exceptions import InvalidApiKeyError, VehicleNotFoundError

VALID_BODY = {
    "vehicle_id": "ALP-001",
    "lat": 4.6097,
    "lng": -74.0817,
    "ts": "2026-11-12T03:15:00Z",
}


class _FakeAuthService:
    def __init__(self, *, valid: bool) -> None:
        self._valid = valid

    def authenticate(self, raw_api_key: str) -> object:
        if not self._valid:
            raise InvalidApiKeyError()
        return object()


class _FakePositionService:
    def __init__(self, *, position: Position | None = None, error: Exception | None = None) -> None:
        self._position = position
        self._error = error

    def register_from_alpha(self, payload: AlphaPayload) -> Position:
        if self._error is not None:
            raise self._error
        assert self._position is not None
        return self._position


def _make_position() -> Position:
    vehicle = Vehicle(uuid=uuid.uuid4(), plate="ABC123", name="Camión 01", alpha_id="ALP-001")
    position = Position(
        uuid=uuid.uuid4(),
        lat=4.6097,
        lng=-74.0817,
        recorded_at=datetime(2026, 11, 12, 3, 15, 0, tzinfo=UTC),
        received_at=datetime(2026, 11, 12, 3, 15, 2, tzinfo=UTC),
        provider=ProviderName.alpha,
    )
    position.vehicle = vehicle
    return position


def test_create_position_valid_request_returns_201(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    app.dependency_overrides[get_position_service] = lambda: _FakePositionService(
        position=_make_position()
    )
    try:
        response = client.post(
            "/providers/alpha/positions",
            json=VALID_BODY,
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {
        "uuid",
        "vehicle_uuid",
        "lat",
        "lng",
        "recorded_at",
        "received_at",
        "provider",
    }
    assert body["provider"] == "alpha"
    assert body["lat"] == 4.6097
    assert body["lng"] == -74.0817


def test_create_position_without_authorization_returns_401(client: TestClient) -> None:
    response = client.post("/providers/alpha/positions", json=VALID_BODY)

    assert response.status_code == 401


def test_create_position_with_malformed_authorization_returns_401(client: TestClient) -> None:
    response = client.post(
        "/providers/alpha/positions",
        json=VALID_BODY,
        headers={"Authorization": "Basic abc"},
    )

    assert response.status_code == 401


def test_create_position_with_invalid_api_key_returns_401(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=False)
    try:
        response = client.post(
            "/providers/alpha/positions",
            json=VALID_BODY,
            headers={"Authorization": "Bearer wrong-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401


def test_create_position_unknown_vehicle_returns_404(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    app.dependency_overrides[get_position_service] = lambda: _FakePositionService(
        error=VehicleNotFoundError(ProviderName.alpha)
    )
    try:
        response = client.post(
            "/providers/alpha/positions",
            json=VALID_BODY,
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found for provider alpha"}


def test_create_position_lat_out_of_range_returns_422(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    try:
        response = client.post(
            "/providers/alpha/positions",
            json={**VALID_BODY, "lat": 91.0},
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


def test_create_position_ts_without_timezone_returns_422(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    try:
        response = client.post(
            "/providers/alpha/positions",
            json={**VALID_BODY, "ts": "2026-11-12T03:15:00"},
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


def test_create_position_missing_required_field_returns_422(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    try:
        response = client.post(
            "/providers/alpha/positions",
            json={"vehicle_id": "ALP-001", "lng": -74.0817, "ts": "2026-11-12T03:15:00Z"},
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
