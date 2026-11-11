from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.repositories.position_repository import PositionRepository
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.services.auth_service import AuthService
from app.services.exceptions import InvalidApiKeyError
from app.services.position_service import PositionService


def get_auth_service(db: Annotated[Session, Depends(get_db)]) -> AuthService:
    return AuthService(UserRepository(db))


def get_position_service(db: Annotated[Session, Depends(get_db)]) -> PositionService:
    return PositionService(VehicleRepository(db), PositionRepository(db))


def _read_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def require_api_key(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    raw_api_key = _read_bearer_token(authorization)
    if raw_api_key is None:
        raise InvalidApiKeyError()
    return auth_service.authenticate(raw_api_key)
