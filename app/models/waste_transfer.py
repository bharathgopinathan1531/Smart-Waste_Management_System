from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class WasteTransfer(Base):
    __tablename__ = "waste_transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    transfer_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    collection_id: Mapped[int] = mapped_column(
        ForeignKey("collection_records.id"), nullable=False, index=True
    )

    recycling_center_id: Mapped[int] = mapped_column(
        ForeignKey("recycling_centers.id"), nullable=False, index=True
    )

    transferred_quantity: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    quantity_unit: Mapped[str] = mapped_column(
        String(20), default="kg", nullable=False
    )

    transfer_type: Mapped[str] = mapped_column(
        String(30), default="direct", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30), default="pending", nullable=False, index=True
    )

    vehicle_id: Mapped[int | None] = mapped_column(
        ForeignKey("vehicles.id"), nullable=True
    )

    transferred_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    received_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    transferred_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    received_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    collection = relationship("CollectionRecord")
    recycling_center = relationship("RecyclingCenter")
    vehicle = relationship("Vehicle")
    transfer_user = relationship("User", foreign_keys=[transferred_by])
    receiver_user = relationship("User", foreign_keys=[received_by])