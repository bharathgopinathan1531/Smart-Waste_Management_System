from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.processing_batch import ProcessingBatch
from app.models.segregation import WasteSegregation
from app.repositories.processing import (
    get_batch_by_id,
    get_all_batches,
    count_batches,
    create_batch,
    update_batch,
    delete_batch,
)


def create_new_batch(
    db: Session,
    batch_data: dict,
    current_user_id: int | None = None,
):
    segregation = (
        db.query(WasteSegregation)
        .filter(WasteSegregation.id == batch_data["segregation_id"])
        .first()
    )

    if not segregation:
        raise ValueError("Segregation record not found")

    if segregation.status != "completed":
        raise ValueError("Only completed segregation records can be processed")

    input_quantity = batch_data["input_quantity"]

    already_processed = (
        db.query(
            func.coalesce(func.sum(ProcessingBatch.input_quantity), 0)
        )
        .filter(ProcessingBatch.segregation_id == segregation.id)
        .filter(ProcessingBatch.status != "cancelled")
        .scalar()
        or 0
    )

    if already_processed + input_quantity > segregation.segregated_quantity:
        raise ValueError(
            "Processing input exceeds the remaining segregated quantity"
        )

    data = batch_data.copy()
    data["batch_number"] = (
        f"BAT-{datetime.now(timezone.utc):%Y%m%d}-{uuid4().hex[:8].upper()}"
    )
    data["recovered_quantity"] = 0
    data["rejected_quantity"] = 0
    data["recovery_rate"] = 0
    data["status"] = "pending"
    data["processed_by"] = current_user_id

    try:
        batch = create_batch(db, data)
        db.commit()
        db.refresh(batch)
        return batch
    except Exception:
        db.rollback()
        raise


def list_batches(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    segregation_id: int | None = None,
):
    filters = {
        "status": status,
        "segregation_id": segregation_id,
    }

    return {
        "total": count_batches(db, **filters),
        "batches": get_all_batches(
            db,
            skip=skip,
            limit=limit,
            **filters,
        ),
    }


def get_batch_details(db: Session, batch_id: int):
    batch = get_batch_by_id(db, batch_id)

    if not batch:
        raise ValueError("Processing batch not found")

    return batch


def update_existing_batch(
    db: Session,
    batch_id: int,
    update_data: dict,
):
    batch = get_batch_details(db, batch_id)

    if batch.status != "pending":
        raise ValueError("Only pending batches can be updated")

    data = {
        key: value
        for key, value in update_data.items()
        if value is not None
    }

    input_quantity = data.get("input_quantity", batch.input_quantity)
    recovered_quantity = data.get(
        "recovered_quantity", batch.recovered_quantity
    )
    rejected_quantity = data.get(
        "rejected_quantity", batch.rejected_quantity
    )

    if recovered_quantity + rejected_quantity > input_quantity:
        raise ValueError(
            "Recovered and rejected quantities cannot exceed input quantity"
        )

    if "input_quantity" in data:
        segregation = (
            db.query(WasteSegregation)
            .filter(WasteSegregation.id == batch.segregation_id)
            .first()
        )

        other_input = (
            db.query(
                func.coalesce(func.sum(ProcessingBatch.input_quantity), 0)
            )
            .filter(ProcessingBatch.segregation_id == batch.segregation_id)
            .filter(ProcessingBatch.id != batch.id)
            .filter(ProcessingBatch.status != "cancelled")
            .scalar()
            or 0
        )

        if other_input + input_quantity > segregation.segregated_quantity:
            raise ValueError(
                "Processing input exceeds the remaining segregated quantity"
            )

    if input_quantity > 0:
        data["recovery_rate"] = round(
            (recovered_quantity / input_quantity) * 100,
            2,
        )

    try:
        updated = update_batch(db, batch, data)
        db.commit()
        db.refresh(updated)
        return updated
    except Exception:
        db.rollback()
        raise


def update_batch_status(
    db: Session,
    batch_id: int,
    new_status: str,
    notes: str | None = None,
):
    batch = get_batch_details(db, batch_id)

    allowed_transitions = {
        "pending": {"in_progress", "cancelled"},
        "in_progress": {"completed", "cancelled"},
        "completed": set(),
        "cancelled": set(),
    }

    if new_status not in allowed_transitions:
        raise ValueError("Invalid processing status")

    if new_status not in allowed_transitions[batch.status]:
        raise ValueError(
            f"Cannot change batch status from {batch.status} to {new_status}"
        )

    try:
        now = datetime.now(timezone.utc)
        batch.status = new_status

        if notes is not None:
            batch.notes = notes

        if new_status == "in_progress":
            batch.started_at = now

        if new_status == "completed":
            if batch.recovered_quantity + batch.rejected_quantity > batch.input_quantity:
                raise ValueError(
                    "Recovered and rejected quantities cannot exceed input quantity"
                )

            batch.recovery_rate = round(
                (batch.recovered_quantity / batch.input_quantity) * 100,
                2,
            )
            batch.completed_at = now

        db.commit()
        db.refresh(batch)
        return batch

    except Exception:
        db.rollback()
        raise


def remove_batch(db: Session, batch_id: int):
    batch = get_batch_details(db, batch_id)

    if batch.status != "pending":
        raise ValueError("Only pending batches can be deleted")

    try:
        delete_batch(db, batch)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise