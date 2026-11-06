from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Enum as SQLAlchemyEnum,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.utils.enums import EnvironmentalImpactStatus


class EnvironmentalImpact(Base):
    __tablename__ = "environmental_impacts"

    id = Column(Integer, primary_key=True, index=True)

    report_number = Column(String(50), unique=True, nullable=False, index=True)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    total_waste_collected_kg = Column(Float, default=0, nullable=False)
    total_waste_recycled_kg = Column(Float, default=0, nullable=False)
    total_waste_disposed_kg = Column(Float, default=0, nullable=False)

    co2_saved_kg = Column(Float, default=0, nullable=False)
    water_saved_liters = Column(Float, default=0, nullable=False)
    energy_saved_kwh = Column(Float, default=0, nullable=False)
    landfill_waste_reduced_kg = Column(Float, default=0, nullable=False)

    calculation_method = Column(Text, nullable=True)

    status = Column(
        SQLAlchemyEnum(EnvironmentalImpactStatus),
        default=EnvironmentalImpactStatus.CALCULATED,
        nullable=False,
    )

    calculated_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    verified_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    verified_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    calculator = relationship(
        "User",
        foreign_keys=[calculated_by],
    )

    verifier = relationship(
        "User",
        foreign_keys=[verified_by],
    )