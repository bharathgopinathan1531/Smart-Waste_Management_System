
from datetime import datetime, time, timedelta, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.collection import CollectionRecord
from app.models.processing_batch import ProcessingBatch
from app.models.disposal import WasteDisposal
from app.models.environmental_impact import EnvironmentalImpact
from app.utils.enums import (
    EnvironmentalImpactStatus,
    DisposalStatus,
    ProcessingStatus,
)


# Demonstration factors only.
# Replace with verified environmental factors before production.
CO2_SAVED_PER_KG_RECYCLED = 0.5
WATER_SAVED_PER_KG_RECYCLED = 2.0
ENERGY_SAVED_PER_KG_RECYCLED = 1.5


def calculate_environmental_impact(
    db: Session,
    start_date,
    end_date,
    calculated_by=None,
):
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")

    start_datetime = datetime.combine(start_date, time.min)
    end_datetime = datetime.combine(
        end_date + timedelta(days=1),
        time.min,
    )

    collections = (
        db.query(CollectionRecord)
        .filter(
            CollectionRecord.collection_completed_at >= start_datetime,
            CollectionRecord.collection_completed_at < end_datetime,
        )
        .all()
    )

    processing_batches = (
        db.query(ProcessingBatch)
        .filter(
            ProcessingBatch.completed_at >= start_datetime,
            ProcessingBatch.completed_at < end_datetime,
            ProcessingBatch.status == ProcessingStatus.COMPLETED,
        )
        .all()
    )

    disposals = (
        db.query(WasteDisposal)
        .filter(
            WasteDisposal.disposal_date >= start_datetime,
            WasteDisposal.disposal_date < end_datetime,
            WasteDisposal.status == DisposalStatus.COMPLETED,
        )
        .all()
    )

    # Calculate collected quantity in kilograms.
    total_collected = 0.0

    for record in collections:
        if str(record.unit).lower() == "kg":
            quantity = float(record.collected_quantity or 0)

            if quantity < 0:
                raise ValueError(
                    "Collected quantity cannot be negative"
                )

            total_collected += quantity

    # Calculate recovered quantity in kilograms.
    total_recycled = 0.0

    for batch in processing_batches:
        if str(batch.quantity_unit).lower() == "kg":
            quantity = float(batch.recovered_quantity or 0)

            if quantity < 0:
                raise ValueError(
                    "Recovered quantity cannot be negative"
                )

            total_recycled += quantity

    # Calculate disposed quantity in kilograms.
    total_disposed = 0.0

    for disposal in disposals:
        if str(disposal.unit).lower() == "kg":
            quantity = float(disposal.quantity or 0)

            if quantity < 0:
                raise ValueError(
                    "Disposed quantity cannot be negative"
                )

            total_disposed += quantity

    # Calculate estimated environmental savings.
    co2_saved = (
        total_recycled * CO2_SAVED_PER_KG_RECYCLED
    )

    water_saved = (
        total_recycled * WATER_SAVED_PER_KG_RECYCLED
    )

    energy_saved = (
        total_recycled * ENERGY_SAVED_PER_KG_RECYCLED
    )

    landfill_reduced = total_recycled

    report_number = (
        f"EIR-{datetime.now(timezone.utc).strftime('%Y%m%d')}-"
        f"{uuid4().hex[:8].upper()}"
    )

    impact = EnvironmentalImpact(
        report_number=report_number,
        start_date=start_date,
        end_date=end_date,
        total_waste_collected_kg=round(total_collected, 2),
        total_waste_recycled_kg=round(total_recycled, 2),
        total_waste_disposed_kg=round(total_disposed, 2),
        co2_saved_kg=round(co2_saved, 2),
        water_saved_liters=round(water_saved, 2),
        energy_saved_kwh=round(energy_saved, 2),
        landfill_waste_reduced_kg=round(landfill_reduced, 2),
        calculation_method=(
            "Estimated using project demonstration factors: "
            "0.5 kg CO2, 2 liters water and 1.5 kWh saved "
            "per kg recycled. Only completed records measured "
            "in kilograms are included."
        ),
        status=EnvironmentalImpactStatus.CALCULATED,
        calculated_by=calculated_by,
    )

    try:
        db.add(impact)
        db.commit()
        db.refresh(impact)
        return impact
    except Exception:
        db.rollback()
        raise


def list_environmental_impacts(
    db: Session,
    skip=0,
    limit=100,
    status=None,
):
    from app.repositories.environmental_impact import (
        get_all_impacts,
        count_impacts,
    )

    items = get_all_impacts(
        db,
        skip=skip,
        limit=limit,
        status=status,
    )

    total = count_impacts(
        db,
        status=status,
    )

    return {
        "total": total,
        "items": items,
    }


def get_environmental_impact(
    db: Session,
    impact_id: int,
):
    impact = (
        db.query(EnvironmentalImpact)
        .filter(EnvironmentalImpact.id == impact_id)
        .first()
    )

    if not impact:
        raise ValueError(
            "Environmental impact report not found"
        )

    return impact


def verify_environmental_impact(
    db: Session,
    impact_id: int,
    verified_by: int,
):
    impact = get_environmental_impact(
        db,
        impact_id,
    )

    if impact.status != EnvironmentalImpactStatus.CALCULATED:
        raise ValueError(
            "Only calculated reports can be verified"
        )

    try:
        impact.status = EnvironmentalImpactStatus.VERIFIED
        impact.verified_by = verified_by
        impact.verified_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(impact)

        return impact
    except Exception:
        db.rollback()
        raise


def delete_environmental_impact(
    db: Session,
    impact_id: int,
):
    impact = get_environmental_impact(
        db,
        impact_id,
    )

    if impact.status == EnvironmentalImpactStatus.VERIFIED:
        raise ValueError(
            "Verified reports cannot be deleted"
        )

    try:
        db.delete(impact)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
