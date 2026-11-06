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
from app.utils.enums import DisposalMethod, DisposalStatus


class WasteDisposal(Base):
    __tablename__ = "waste_disposals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    disposal_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    processing_batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("processing_batches.id", ondelete="SET NULL"),
        nullable=True,
    )

    transfer_id: Mapped[int | None] = mapped_column(
        ForeignKey("waste_transfers.id", ondelete="SET NULL"),
        nullable=True,
    )

    waste_category_id: Mapped[int] = mapped_column(
        ForeignKey("waste_categories.id"),
        nullable=False,
    )

    disposal_method: Mapped[DisposalMethod] = mapped_column(
        SQLEnum(DisposalMethod),
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(Float, nullable=False)

    quantity_unit: Mapped[str] = mapped_column(
        String(20), default="kg", nullable=False
    )

    disposal_location: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    disposal_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    status: Mapped[DisposalStatus] = mapped_column(
        SQLEnum(DisposalStatus),
        default=DisposalStatus.PENDING,
        nullable=False,
    )

    recorded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    approved_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    processing_batch = relationship("ProcessingBatch")
    transfer = relationship("WasteTransfer")
    waste_category = relationship("WasteCategory")

    recorder = relationship(
        "User",
        foreign_keys=[recorded_by],
    )

    approver = relationship(
        "User",
        foreign_keys=[approved_by],
    )