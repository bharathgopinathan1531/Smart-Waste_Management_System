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


class ProcessingBatch(Base):
    __tablename__ = "processing_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    batch_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    segregation_id: Mapped[int] = mapped_column(
        ForeignKey("waste_segregations.id"),
        nullable=False,
        index=True,
    )

    processing_method: Mapped[str] = mapped_column(
        String(30), default="sorting", nullable=False
    )

    input_quantity: Mapped[float] = mapped_column(Float, nullable=False)

    recovered_quantity: Mapped[float] = mapped_column(
        Float, default=0, nullable=False
    )

    rejected_quantity: Mapped[float] = mapped_column(
        Float, default=0, nullable=False
    )

    quantity_unit: Mapped[str] = mapped_column(
        String(20), default="kg", nullable=False
    )

    recovery_rate: Mapped[float] = mapped_column(
        Float, default=0, nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30), default="pending", nullable=False, index=True
    )

    processed_by: Mapped[int | None] = mapped_column(
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

    segregation = relationship("WasteSegregation")
    processor = relationship("User")