import uuid
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.adapters.beta import BetaPayload
from app.api.dependencies import get_auth_service, get_position_service
from app.main import app
from app.models import Position, Vehicle
from app.models.enums import ProviderName
from app.services.exceptions import InvalidApiKeyError, VehicleNotFoundError

VALID_BODY = {
    "unit_code": "BT-9001",
    "coords": {"latitude": 4.6533, "longitude": -74.0836},
    "epoch": 1794452100,
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

    def register_from_beta(self, payload: BetaPayload) -> Position:
        if self._error is not None:
            raise self._error
        assert self._position is not None
        return self._position


def _make_position() -> Position:
    vehicle = Vehicle(uuid=uuid.uuid4(), plate="GHI789", name="Camión 03", beta_code="BT-9001")
    position = Position(
        uuid=uuid.uuid4(),
        lat=4.6533,
        lng=-74.0836,
        recorded_at=datetime(2026, 11, 12, 2, 55, 0, tzinfo=UTC),
        received_at=datetime(2026, 11, 12, 2, 55, 2, tzinfo=UTC),
        provider=ProviderName.beta,
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
            "/providers/beta/positions",
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
    assert body["provider"] == "beta"
    assert body["lat"] == 4.6533
    assert body["lng"] == -74.0836


def test_create_position_without_authorization_returns_401(client: TestClient) -> None:
    response = client.post("/providers/beta/positions", json=VALID_BODY)

    assert response.status_code == 401


def test_create_position_unknown_vehicle_returns_404(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    app.dependency_overrides[get_position_service] = lambda: _FakePositionService(
        error=VehicleNotFoundError(ProviderName.beta)
    )
    try:
        response = client.post(
            "/providers/beta/positions",
            json=VALID_BODY,
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found for provider beta"}


def test_create_position_latitude_out_of_range_returns_422(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    try:
        response = client.post(
            "/providers/beta/positions",
            json={**VALID_BODY, "coords": {"latitude": 91.0, "longitude": -74.0836}},
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


def test_create_position_missing_coords_returns_422(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    try:
        response = client.post(
            "/providers/beta/positions",
            json={"unit_code": "BT-9001", "epoch": 1794452100},
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


def test_create_position_epoch_non_integer_returns_422(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    try:
        response = client.post(
            "/providers/beta/positions",
            json={**VALID_BODY, "epoch": 1.5},
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


def test_create_position_epoch_non_positive_returns_422(client: TestClient) -> None:
    app.dependency_overrides[get_auth_service] = lambda: _FakeAuthService(valid=True)
    try:
        response = client.post(
            "/providers/beta/positions",
            json={**VALID_BODY, "epoch": 0},
            headers={"Authorization": "Bearer test-key"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
