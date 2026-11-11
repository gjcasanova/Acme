from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Index, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ProviderName

if TYPE_CHECKING:
    from app.models.vehicle import Vehicle


class Position(Base):
    __tablename__ = "positions"
    __table_args__ = (Index("ix_positions_vehicle_id_recorded_at", "vehicle_id", "recorded_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), unique=True, index=True, default=uuid.uuid4, nullable=False
    )
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    provider: Mapped[ProviderName] = mapped_column(
        Enum(
            ProviderName,
            native_enum=False,
            values_callable=lambda cls: [member.value for member in cls],
            validate_strings=True,
        ),
        nullable=False,
    )

    vehicle: Mapped[Vehicle] = relationship(back_populates="positions")

    @property
    def vehicle_uuid(self) -> uuid.UUID:
        return self.vehicle.uuid
