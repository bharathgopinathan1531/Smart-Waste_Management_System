from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.disposal import WasteDisposal
from app.models.processing_batch import ProcessingBatch
from app.models.waste_transfer import WasteTransfer
from app.models.segregation import WasteSegregation
from app.models.waste_category import WasteCategory
from app.repositories.disposal import (
    get_disposal_by_id,
    get_all_disposals,
    count_disposals,
    create_disposal,
    update_disposal,
    delete_disposal,
)


def create_new_disposal(
    db: Session,
    disposal_data: dict,
    current_user_id: int,
):
    data = disposal_data.copy()

    if not data.get("processing_batch_id") and not data.get("transfer_id"):
        raise ValueError(
            "Either a processing batch or a waste transfer must be provided"
        )

    category = (
        db.query(WasteCategory)
        .filter(WasteCategory.id == data["waste_category_id"])
        .first()
    )

    if not category or category.status != "active":
        raise ValueError("Active waste category not found")

    if data.get("processing_batch_id"):
        batch = (
            db.query(ProcessingBatch)
            .filter(
                ProcessingBatch.id == data["processing_batch_id"]
            )
            .first()
        )

        if not batch:
            raise ValueError("Processing batch not found")

        if batch.status != "completed":
            raise ValueError("Only completed processing batches can be disposed")

        if batch.segregation.waste_category_id != data["waste_category_id"]:
            raise ValueError("Waste category does not match the processing batch")

        already_disposed = (
            db.query(
                func.coalesce(func.sum(WasteDisposal.quantity), 0)
            )
            .filter(
                WasteDisposal.processing_batch_id == batch.id,
                WasteDisposal.status != "cancelled",
            )
            .scalar()
            or 0
        )

        available_quantity = (
            batch.input_quantity
            - batch.recovered_quantity
            - already_disposed
        )

        if data["quantity"] > available_quantity:
            raise ValueError(
                "Disposal quantity exceeds the remaining processing waste"
            )

    if data.get("transfer_id"):
        transfer = (
            db.query(WasteTransfer)
            .filter(WasteTransfer.id == data["transfer_id"])
            .first()
        )

        if not transfer:
            raise ValueError("Waste transfer not found")

        if transfer.status != "received":
            raise ValueError("Only received waste transfers can be disposed")

        already_disposed = (
            db.query(
                func.coalesce(func.sum(WasteDisposal.quantity), 0)
            )
            .filter(
                WasteDisposal.transfer_id == transfer.id,
                WasteDisposal.status != "cancelled",
            )
            .scalar()
            or 0
        )

        already_segregated = (
            db.query(
                func.coalesce(func.sum(WasteSegregation.segregated_quantity), 0)
            )
            .filter(
                WasteSegregation.transfer_id == transfer.id,
                WasteSegregation.status != "cancelled",
            )
            .scalar()
            or 0
        )

        available_quantity = (
            transfer.transferred_quantity
            - already_segregated
            - already_disposed
        )

        if data["quantity"] > available_quantity:
            raise ValueError(
                "Disposal quantity exceeds the remaining unsegregated waste"
            )

    disposal_date = data["disposal_date"]

    if disposal_date.tzinfo is None:
        disposal_date = disposal_date.replace(tzinfo=timezone.utc)

    if disposal_date > datetime.now(timezone.utc):
        raise ValueError("Disposal date cannot be in the future")

    data["disposal_date"] = disposal_date
    data["disposal_number"] = (
        f"DSP-{datetime.now(timezone.utc):%Y%m%d}-{uuid4().hex[:8].upper()}"
    )
    data["status"] = "pending"
    data["recorded_by"] = current_user_id
    data["approved_by"] = None

    try:
        disposal = create_disposal(db, data)
        db.commit()
        db.refresh(disposal)
        return disposal
    except Exception:
        db.rollback()
        raise


def list_disposals(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    waste_category_id: int | None = None,
    disposal_method: str | None = None,
):
    filters = {
        "status": status,
        "waste_category_id": waste_category_id,
        "disposal_method": disposal_method,
    }

    return {
        "total": count_disposals(db, **filters),
        "disposals": get_all_disposals(
            db,
            skip=skip,
            limit=limit,
            **filters,
        ),
    }


def get_disposal_details(db: Session, disposal_id: int):
    disposal = get_disposal_by_id(db, disposal_id)

    if not disposal:
        raise ValueError("Disposal record not found")

    return disposal


def update_existing_disposal(
    db: Session,
    disposal_id: int,
    update_data: dict,
):
    disposal = get_disposal_details(db, disposal_id)

    if disposal.status != "pending":
        raise ValueError("Only pending disposal records can be updated")

    data = {
        key: value
        for key, value in update_data.items()
        if value is not None
    }

    if "quantity" in data:
        batch_id = disposal.processing_batch_id
        transfer_id = disposal.transfer_id

        if batch_id:
            batch = (
                db.query(ProcessingBatch)
                .filter(ProcessingBatch.id == batch_id)
                .first()
            )

            other_disposed = (
                db.query(func.coalesce(func.sum(WasteDisposal.quantity), 0))
                .filter(
                    WasteDisposal.processing_batch_id == batch_id,
                    WasteDisposal.id != disposal.id,
                    WasteDisposal.status != "cancelled",
                )
                .scalar()
                or 0
            )

            available = (
                batch.input_quantity
                - batch.recovered_quantity
                - other_disposed
            )

        else:
            transfer = (
                db.query(WasteTransfer)
                .filter(WasteTransfer.id == transfer_id)
                .first()
            )

            other_disposed = (
                db.query(func.coalesce(func.sum(WasteDisposal.quantity), 0))
                .filter(
                    WasteDisposal.transfer_id == transfer_id,
                    WasteDisposal.id != disposal.id,
                    WasteDisposal.status != "cancelled",
                )
                .scalar()
                or 0
            )

            segregated = (
                db.query(
                    func.coalesce(
                        func.sum(WasteSegregation.segregated_quantity), 0
                    )
                )
                .filter(
                    WasteSegregation.transfer_id == transfer_id,
                    WasteSegregation.status != "cancelled",
                )
                .scalar()
                or 0
            )

            available = (
                transfer.transferred_quantity
                - segregated
                - other_disposed
            )

        if data["quantity"] > available:
            raise ValueError("Disposal quantity exceeds the available quantity")

    if "disposal_date" in data:
        disposal_date = data["disposal_date"]

        if disposal_date.tzinfo is None:
            disposal_date = disposal_date.replace(tzinfo=timezone.utc)

        if disposal_date > datetime.now(timezone.utc):
            raise ValueError("Disposal date cannot be in the future")

        data["disposal_date"] = disposal_date

    try:
        updated = update_disposal(db, disposal, data)
        db.commit()
        db.refresh(updated)
        return updated
    except Exception:
        db.rollback()
        raise


def update_disposal_status(
    db: Session,
    disposal_id: int,
    new_status: str,
    current_user_id: int,
    notes: str | None = None,
):
    disposal = get_disposal_details(db, disposal_id)

    allowed_transitions = {
        "pending": {"approved", "cancelled"},
        "approved": {"completed", "cancelled"},
        "completed": set(),
        "cancelled": set(),
    }

    if new_status not in allowed_transitions:
        raise ValueError("Invalid disposal status")

    if new_status not in allowed_transitions[disposal.status]:
        raise ValueError(
            f"Cannot change disposal status from {disposal.status} to {new_status}"
        )

    try:
        disposal.status = new_status

        if notes is not None:
            disposal.notes = notes

        if new_status == "approved":
            disposal.approved_by = current_user_id

        db.commit()
        db.refresh(disposal)
        return disposal
    except Exception:
        db.rollback()
        raise


def remove_disposal(db: Session, disposal_id: int):
    disposal = get_disposal_details(db, disposal_id)

    if disposal.status not in {"pending", "cancelled"}:
        raise ValueError(
            "Only pending or cancelled disposal records can be deleted"
        )

    try:
        delete_disposal(db, disposal)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise