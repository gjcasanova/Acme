from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_api_key_hash(self, api_key_hash: str) -> User | None:
        return self._db.scalar(select(User).where(User.api_key_hash == api_key_hash))
