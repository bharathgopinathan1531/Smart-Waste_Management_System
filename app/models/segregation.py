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


class WasteSegregation(Base):
    __tablename__ = "waste_segregations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    segregation_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    transfer_id: Mapped[int] = mapped_column(
        ForeignKey("waste_transfers.id"),
        nullable=False,
        index=True,
    )

    waste_category_id: Mapped[int] = mapped_column(
        ForeignKey("waste_categories.id"),
        nullable=False,
        index=True,
    )

    segregated_quantity: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    quantity_unit: Mapped[str] = mapped_column(
        String(20), default="kg", nullable=False
    )

    quality: Mapped[str] = mapped_column(
        String(30), default="good", nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30), default="pending", nullable=False, index=True
    )

    segregated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
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

    transfer = relationship("WasteTransfer")
    waste_category = relationship("WasteCategory")
    worker = relationship("User")