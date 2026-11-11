from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.exceptions import InvalidApiKeyError


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


def _read_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def require_api_key(
    authorization: str | None = Header(default=None),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    raw_api_key = _read_bearer_token(authorization)
    if raw_api_key is None:
        raise InvalidApiKeyError()
    return auth_service.authenticate(raw_api_key)
