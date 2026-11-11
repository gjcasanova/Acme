from sqlalchemy.orm import Session

from app.models import Position


class PositionRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def add(self, position: Position) -> Position:
        self._db.add(position)
        self._db.commit()
        return position
