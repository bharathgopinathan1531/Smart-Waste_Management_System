from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.utils.enums import (
    MaintenanceType,
    MaintenanceStatus,
    MaintenancePriority,
)


class VehicleMaintenance(Base):
    __tablename__ = "vehicle_maintenance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    maintenance_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    maintenance_type: Mapped[MaintenanceType] = mapped_column(
        SQLEnum(MaintenanceType),
        nullable=False,
    )

    priority: Mapped[MaintenancePriority] = mapped_column(
        SQLEnum(MaintenancePriority),
        default=MaintenancePriority.NORMAL,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    scheduled_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    service_provider: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    cost: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    odometer_reading: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    status: Mapped[MaintenanceStatus] = mapped_column(
        SQLEnum(MaintenanceStatus),
        default=MaintenanceStatus.SCHEDULED,
        nullable=False,
    )

    reported_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    vehicle = relationship("Vehicle")

    reporter = relationship(
        "User",
        foreign_keys=[reported_by],
    )