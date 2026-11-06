from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.segregation import WasteSegregation
from app.models.waste_transfer import WasteTransfer
from app.models.waste_category import WasteCategory
from app.repositories.segregation import (
    get_segregation_by_id,
    get_all_segregations,
    count_segregations,
    create_segregation,
    update_segregation,
    delete_segregation,
)


def create_new_segregation(
    db: Session,
    segregation_data: dict,
    current_user_id: int | None = None,
):
    transfer = (
        db.query(WasteTransfer)
        .filter(WasteTransfer.id == segregation_data["transfer_id"])
        .first()
    )

    if not transfer:
        raise ValueError("Waste transfer not found")

    if transfer.status != "received":
        raise ValueError("Waste must be received before segregation")

    category = (
        db.query(WasteCategory)
        .filter(
            WasteCategory.id == segregation_data["waste_category_id"]
        )
        .first()
    )

    if not category:
        raise ValueError("Waste category not found")

    if category.status != "active":
        raise ValueError("Waste category is not active")

    quantity = segregation_data["segregated_quantity"]

    already_segregated = (
        db.query(func.coalesce(func.sum(WasteSegregation.segregated_quantity), 0))
        .filter(WasteSegregation.transfer_id == transfer.id)
        .filter(WasteSegregation.status != "cancelled")
        .scalar()
        or 0
    )

    if already_segregated + quantity > transfer.transferred_quantity:
        raise ValueError(
            "Segregated quantity exceeds the remaining received quantity"
        )

    data = segregation_data.copy()
    data["segregation_number"] = (
        f"SEG-{datetime.now(timezone.utc):%Y%m%d}-{uuid4().hex[:8].upper()}"
    )
    data["status"] = "pending"
    data["segregated_by"] = current_user_id

    try:
        segregation = create_segregation(db, data)
        db.commit()
        db.refresh(segregation)
        return segregation
    except Exception:
        db.rollback()
        raise


def list_segregations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    transfer_id: int | None = None,
    waste_category_id: int | None = None,
):
    filters = {
        "status": status,
        "transfer_id": transfer_id,
        "waste_category_id": waste_category_id,
    }

    return {
        "total": count_segregations(db, **filters),
        "segregations": get_all_segregations(
            db,
            skip=skip,
            limit=limit,
            **filters,
        ),
    }


def get_segregation_details(db: Session, segregation_id: int):
    segregation = get_segregation_by_id(db, segregation_id)

    if not segregation:
        raise ValueError("Segregation record not found")

    return segregation


def update_existing_segregation(
    db: Session,
    segregation_id: int,
    update_data: dict,
):
    segregation = get_segregation_details(db, segregation_id)

    if segregation.status != "pending":
        raise ValueError("Only pending segregation records can be updated")

    update_data = {
        key: value
        for key, value in update_data.items()
        if value is not None
    }

    if "segregated_quantity" in update_data:
        transfer = (
            db.query(WasteTransfer)
            .filter(WasteTransfer.id == segregation.transfer_id)
            .first()
        )

        other_quantity = (
            db.query(
                func.coalesce(func.sum(WasteSegregation.segregated_quantity), 0)
            )
            .filter(WasteSegregation.transfer_id == segregation.transfer_id)
            .filter(WasteSegregation.id != segregation.id)
            .filter(WasteSegregation.status != "cancelled")
            .scalar()
            or 0
        )

        if other_quantity + update_data["segregated_quantity"] > transfer.transferred_quantity:
            raise ValueError("Segregated quantity exceeds received quantity")

    try:
        updated = update_segregation(db, segregation, update_data)
        db.commit()
        db.refresh(updated)
        return updated
    except Exception:
        db.rollback()
        raise


def update_segregation_status(
    db: Session,
    segregation_id: int,
    new_status: str,
    notes: str | None = None,
):
    segregation = get_segregation_details(db, segregation_id)

    allowed_transitions = {
        "pending": {"in_progress", "cancelled"},
        "in_progress": {"completed", "cancelled"},
        "completed": set(),
        "cancelled": set(),
    }

    if new_status not in allowed_transitions:
        raise ValueError("Invalid segregation status")

    if new_status not in allowed_transitions[segregation.status]:
        raise ValueError(
            f"Cannot change segregation status from {segregation.status} to {new_status}"
        )

    try:
        now = datetime.now(timezone.utc)
        segregation.status = new_status

        if notes is not None:
            segregation.notes = notes

        if new_status == "in_progress":
            segregation.started_at = now

        if new_status == "completed":
            segregation.completed_at = now

        db.commit()
        db.refresh(segregation)
        return segregation
    except Exception:
        db.rollback()
        raise


def remove_segregation(db: Session, segregation_id: int):
    segregation = get_segregation_details(db, segregation_id)

    if segregation.status != "pending":
        raise ValueError("Only pending segregation records can be deleted")

    try:
        delete_segregation(db, segregation)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise