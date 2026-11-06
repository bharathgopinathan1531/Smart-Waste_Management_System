from datetime import datetime, time, timezone

from sqlalchemy.orm import Session

from app.models.collection import CollectionRecord
from app.models.assignment import CollectionAssignment
from app.models.vehicle import Vehicle
from app.models.processing_batch import ProcessingBatch
from app.models.waste_category import WasteCategory
from app.models.segregation import WasteSegregation


def _date_range(start_date, end_date):
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")

    start_datetime = datetime.combine(
        start_date, time.min
    )

    end_datetime = datetime.combine(
        end_date, time.max
    )

    return start_datetime, end_datetime


def get_collection_report(db: Session, start_date, end_date):
    start_datetime, end_datetime = _date_range(
        start_date, end_date
    )

    records = (
        db.query(CollectionRecord)
        .filter(
            CollectionRecord.collection_completed_at >= start_datetime,
            CollectionRecord.collection_completed_at <= end_datetime,
        )
        .order_by(CollectionRecord.collection_completed_at.desc())
        .all()
    )

    total_quantity = sum(
        float(record.collected_quantity or 0)
        for record in records
    )

    return {
        "report_type": "collection_report",
        "start_date": start_date,
        "end_date": end_date,
        "total_records": len(records),
        "total_quantity_kg": total_quantity,
        "generated_at": datetime.now(timezone.utc),
        "data": [
            {
                "collection_number": record.collection_number,
                "collected_quantity": float(record.collected_quantity),
                "unit": record.unit,
                "collection_completed_at": record.collection_completed_at,
            }
            for record in records
        ],
    }


def get_waste_category_report(db: Session, start_date, end_date):
    start_datetime, end_datetime = _date_range(
        start_date, end_date
    )

    rows = (
        db.query(
            WasteCategory.name,
            CollectionRecord.unit,
            CollectionRecord.collected_quantity,
        )
        .join(
            CollectionAssignment,
            CollectionRecord.assignment_id == CollectionAssignment.id,
        )
        .join(
            WasteCategory,
            CollectionAssignment.pickup_request.has(),
        )
        .filter(
            CollectionRecord.collection_completed_at >= start_datetime,
            CollectionRecord.collection_completed_at <= end_datetime,
        )
        .all()
    )

    totals = {}

    for category_name, unit, quantity in rows:
        key = (category_name, unit)
        totals[key] = totals.get(key, 0.0) + float(quantity or 0)

    data = [
        {
            "category_name": category_name,
            "total_quantity": quantity,
            "unit": unit,
        }
        for (category_name, unit), quantity in totals.items()
    ]

    return {
        "report_type": "waste_category_report",
        "start_date": start_date,
        "end_date": end_date,
        "total_records": len(data),
        "total_quantity_kg": sum(
            item["total_quantity"] for item in data
        ),
        "generated_at": datetime.now(timezone.utc),
        "data": data,
    }


def get_vehicle_report(db: Session, start_date, end_date):
    start_datetime, end_datetime = _date_range(
        start_date, end_date
    )

    vehicles = db.query(Vehicle).all()
    data = []

    for vehicle in vehicles:
        records = (
            db.query(CollectionRecord)
            .join(
                CollectionAssignment,
                CollectionRecord.assignment_id == CollectionAssignment.id,
            )
            .filter(
                CollectionAssignment.vehicle_id == vehicle.id,
                CollectionRecord.collection_completed_at >= start_datetime,
                CollectionRecord.collection_completed_at <= end_datetime,
            )
            .all()
        )

        data.append({
            "registration_number": vehicle.registration_number,
            "vehicle_name": vehicle.vehicle_name,
            "total_collections": len(records),
            "total_quantity_kg": sum(
                float(record.collected_quantity or 0)
                for record in records
            ),
        })

    return {
        "report_type": "vehicle_report",
        "start_date": start_date,
        "end_date": end_date,
        "total_records": len(data),
        "total_quantity_kg": sum(
            item["total_quantity_kg"] for item in data
        ),
        "generated_at": datetime.now(timezone.utc),
        "data": data,
    }


def get_recycling_report(db: Session, start_date, end_date):
    start_datetime, end_datetime = _date_range(
        start_date, end_date
    )

    batches = (
        db.query(ProcessingBatch)
        .filter(
            ProcessingBatch.created_at >= start_datetime,
            ProcessingBatch.created_at <= end_datetime,
        )
        .order_by(ProcessingBatch.created_at.desc())
        .all()
    )

    data = [
        {
            "batch_number": batch.batch_number,
            "input_quantity": float(batch.input_quantity or 0),
            "recovered_quantity": float(batch.recovered_quantity or 0),
            "rejected_quantity": float(batch.rejected_quantity or 0),
            "recovery_rate": float(batch.recovery_rate or 0),
            "status": str(batch.status),
        }
        for batch in batches
    ]

    return {
        "report_type": "recycling_report",
        "start_date": start_date,
        "end_date": end_date,
        "total_records": len(data),
        "total_quantity_kg": sum(
            item["recovered_quantity"] for item in data
        ),
        "generated_at": datetime.now(timezone.utc),
        "data": data,
    }