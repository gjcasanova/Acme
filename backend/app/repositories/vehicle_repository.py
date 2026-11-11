from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Vehicle
from app.models.enums import ProviderName


class VehicleRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_external_id(self, provider: ProviderName, external_id: str) -> Vehicle | None:
        column = Vehicle.alpha_id if provider == ProviderName.alpha else Vehicle.beta_code
        return self._db.scalar(select(Vehicle).where(column == external_id))
