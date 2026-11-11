import pytest
from sqlalchemy.orm import Session

from app.core.security import hash_api_key
from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.exceptions import InvalidApiKeyError

RAW_API_KEY = "test-api-key-123"


def _create_user(db: Session, *, active: bool) -> None:
    db.add(User(name="Tester", api_key_hash=hash_api_key(RAW_API_KEY), is_active=active))
    db.commit()


def test_authenticate_valid_active_key_returns_user(db_session: Session) -> None:
    _create_user(db_session, active=True)
    service = AuthService(UserRepository(db_session))

    user = service.authenticate(RAW_API_KEY)

    assert user.name == "Tester"


def test_authenticate_unknown_key_raises_invalid_api_key_error(db_session: Session) -> None:
    _create_user(db_session, active=True)
    service = AuthService(UserRepository(db_session))

    with pytest.raises(InvalidApiKeyError):
        service.authenticate("unknown-key")


def test_authenticate_inactive_user_key_raises_invalid_api_key_error(db_session: Session) -> None:
    _create_user(db_session, active=False)
    service = AuthService(UserRepository(db_session))

    with pytest.raises(InvalidApiKeyError):
        service.authenticate(RAW_API_KEY)
