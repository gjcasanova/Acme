from app.core.security import hash_api_key
from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.exceptions import InvalidApiKeyError


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def authenticate(self, raw_api_key: str) -> User:
        user = self._user_repository.get_by_api_key_hash(hash_api_key(raw_api_key))
        if user is None or not user.is_active:
            raise InvalidApiKeyError()
        return user
