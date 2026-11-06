from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.waste_transfer import WasteTransfer
from app.models.collection import CollectionRecord
from app.models.recycling_center import RecyclingCenter
from app.models.vehicle import Vehicle
from app.repositories.transfer import (
    get_transfer_by_id,
    get_all_transfers,
    count_transfers,
    create_transfer,
    update_transfer,
    delete_transfer,
)


def create_new_transfer(
    db: Session,
    transfer_data: dict,
    current_user_id: int | None = None,
):
    collection = (
        db.query(CollectionRecord)
        .filter(CollectionRecord.id == transfer_data["collection_id"])
        .first()
    )

    if not collection:
        raise ValueError("Collection record not found")

    center = (
        db.query(RecyclingCenter)
        .filter(
            RecyclingCenter.id == transfer_data["recycling_center_id"]
        )
        .first()
    )

    if not center:
        raise ValueError("Recycling center not found")

    if center.status != "active":
        raise ValueError("Recycling center is not active")

    quantity = transfer_data["transferred_quantity"]

    existing_quantity = (
        db.query(WasteTransfer)
        .filter(WasteTransfer.collection_id == collection.id)
        .filter(WasteTransfer.status != "cancelled")
        .with_entities(
            __import__("sqlalchemy").func.coalesce(
                __import__("sqlalchemy").func.sum(
                    WasteTransfer.transferred_quantity
                ),
                0,
            )
        )
        .scalar()
        or 0
    )

    if existing_quantity + quantity > collection.collected_quantity:
        raise ValueError(
            "Transfer quantity exceeds the remaining collected quantity"
        )

    if quantity > center.available_capacity_kg:
        raise ValueError("Insufficient recycling center capacity")

    vehicle_id = transfer_data.get("vehicle_id")
    if vehicle_id is not None:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

        if not vehicle:
            raise ValueError("Vehicle not found")

        if vehicle.status != "available":
            raise ValueError("Selected vehicle is not available")

    transfer_data = transfer_data.copy()
    transfer_data["transfer_number"] = (
        f"TRF-{datetime.now(timezone.utc):%Y%m%d}-{uuid4().hex[:8].upper()}"
    )
    transfer_data["status"] = "pending"
    transfer_data["transferred_by"] = current_user_id

    try:
        center.available_capacity_kg -= quantity

        transfer = create_transfer(db, transfer_data)
        db.commit()
        db.refresh(transfer)
        return transfer

    except Exception:
        db.rollback()
        raise


def list_transfers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    recycling_center_id: int | None = None,
    collection_id: int | None = None,
):
    filters = {
        "status": status,
        "recycling_center_id": recycling_center_id,
        "collection_id": collection_id,
    }

    transfers = get_all_transfers(
        db,
        skip=skip,
        limit=limit,
        **filters,
    )

    total = count_transfers(db, **filters)

    return {
        "total": total,
        "transfers": transfers,
    }


def get_transfer_details(db: Session, transfer_id: int):
    transfer = get_transfer_by_id(db, transfer_id)

    if not transfer:
        raise ValueError("Waste transfer not found")

    return transfer


def update_existing_transfer(
    db: Session,
    transfer_id: int,
    update_data: dict,
):
    transfer = get_transfer_details(db, transfer_id)

    if transfer.status != "pending":
        raise ValueError("Only pending transfers can be updated")

    update_data = {
        key: value
        for key, value in update_data.items()
        if value is not None
    }

    center = (
        db.query(RecyclingCenter)
        .filter(RecyclingCenter.id == transfer.recycling_center_id)
        .first()
    )

    if "transferred_quantity" in update_data:
        new_quantity = update_data["transferred_quantity"]
        difference = new_quantity - transfer.transferred_quantity

        if difference > center.available_capacity_kg:
            raise ValueError("Insufficient recycling center capacity")

        center.available_capacity_kg -= difference

        collection = (
            db.query(CollectionRecord)
            .filter(CollectionRecord.id == transfer.collection_id)
            .first()
        )

        other_quantity = (
            db.query(WasteTransfer)
            .filter(WasteTransfer.collection_id == transfer.collection_id)
            .filter(WasteTransfer.id != transfer.id)
            .filter(WasteTransfer.status != "cancelled")
            .with_entities(
                __import__("sqlalchemy").func.coalesce(
                    __import__("sqlalchemy").func.sum(
                        WasteTransfer.transferred_quantity
                    ),
                    0,
                )
            )
            .scalar()
            or 0
        )

        if other_quantity + new_quantity > collection.collected_quantity:
            raise ValueError("Transfer quantity exceeds collected quantity")

    try:
        updated = update_transfer(db, transfer, update_data)
        db.commit()
        db.refresh(updated)
        return updated

    except Exception:
        db.rollback()
        raise


def update_transfer_status(
    db: Session,
    transfer_id: int,
    new_status: str,
    current_user_id: int | None = None,
    notes: str | None = None,
):
    transfer = get_transfer_details(db, transfer_id)

    allowed_transitions = {
        "pending": {"in_transit", "cancelled"},
        "in_transit": {"received", "cancelled"},
        "received": set(),
        "cancelled": set(),
    }

    if new_status not in allowed_transitions:
        raise ValueError("Invalid transfer status")

    if new_status not in allowed_transitions[transfer.status]:
        raise ValueError(
            f"Cannot change transfer status from {transfer.status} to {new_status}"
        )

    try:
        now = datetime.now(timezone.utc)

        transfer.status = new_status

        if notes is not None:
            transfer.notes = notes

        if new_status == "in_transit":
            transfer.transferred_at = now

        elif new_status == "received":
            transfer.received_at = now
            transfer.received_by = current_user_id

        elif new_status == "cancelled":
            center = (
                db.query(RecyclingCenter)
                .filter(
                    RecyclingCenter.id == transfer.recycling_center_id
                )
                .first()
            )

            if center:
                center.available_capacity_kg += transfer.transferred_quantity

                if center.available_capacity_kg > center.total_capacity_kg:
                    center.available_capacity_kg = center.total_capacity_kg

        db.commit()
        db.refresh(transfer)
        return transfer

    except Exception:
        db.rollback()
        raise


def remove_transfer(db: Session, transfer_id: int):
    transfer = get_transfer_details(db, transfer_id)

    if transfer.status != "pending":
        raise ValueError("Only pending transfers can be deleted")

    try:
        center = (
            db.query(RecyclingCenter)
            .filter(
                RecyclingCenter.id == transfer.recycling_center_id
            )
            .first()
        )

        if center:
            center.available_capacity_kg += transfer.transferred_quantity

            if center.available_capacity_kg > center.total_capacity_kg:
                center.available_capacity_kg = center.total_capacity_kg

        delete_transfer(db, transfer)
        db.commit()
        return True

    except Exception:
        db.rollback()
        raise