from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    name: Mapped[str] = mapped_column(
        String(150), nullable=False, index=True
    )

    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    location_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    city: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    state: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )

    latitude: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("locations.id"),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20), default="active", nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    parent = relationship(
        "Location",
        remote_side="Location.id",
        backref="children"
    )