from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.models import Position, Vehicle
from app.models.enums import ProviderName


class VehicleRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_external_id(self, provider: ProviderName, external_id: str) -> Vehicle | None:
        column = Vehicle.alpha_id if provider == ProviderName.alpha else Vehicle.beta_code
        return self._db.scalar(select(Vehicle).where(column == external_id))

    def list_with_last_position(self) -> list[tuple[Vehicle, Position | None]]:
        ranked = select(
            Position.id.label("position_id"),
            Position.vehicle_id.label("vehicle_id"),
            func.row_number()
            .over(
                partition_by=Position.vehicle_id,
                order_by=(Position.recorded_at.desc(), Position.received_at.desc()),
            )
            .label("rn"),
        ).subquery()

        statement = (
            select(Vehicle, Position)
            .select_from(Vehicle)
            .outerjoin(ranked, and_(ranked.c.vehicle_id == Vehicle.id, ranked.c.rn == 1))
            .outerjoin(Position, Position.id == ranked.c.position_id)
            .order_by(Vehicle.plate.asc())
        )
        return self._db.execute(statement).all()
