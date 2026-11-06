from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.models.maintenance import VehicleMaintenance
from app.repositories.maintenance import (
    get_maintenance_by_id,
    get_all_maintenance,
    count_maintenance,
    create_maintenance,
    update_maintenance,
    delete_maintenance,
)


def create_new_maintenance(
    db: Session,
    maintenance_data: dict,
    current_user_id: int,
):
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == maintenance_data["vehicle_id"])
        .first()
    )

    if not vehicle:
        raise ValueError("Vehicle not found")

    if vehicle.status == "on_route":
        raise ValueError(
            "Vehicle currently on route cannot be scheduled for maintenance"
        )

    if vehicle.status == "inactive":
        raise ValueError("Inactive vehicle cannot be scheduled for maintenance")

    active_maintenance = (
        db.query(VehicleMaintenance)
        .filter(
            VehicleMaintenance.vehicle_id == vehicle.id,
            VehicleMaintenance.status.in_(["scheduled", "in_progress"]),
        )
        .first()
    )

    if active_maintenance:
        raise ValueError(
            "Vehicle already has an active maintenance record"
        )

    scheduled_date = maintenance_data["scheduled_date"]

    if scheduled_date.tzinfo is None:
        scheduled_date = scheduled_date.replace(tzinfo=timezone.utc)

    if scheduled_date < datetime.now(timezone.utc):
        raise ValueError("Scheduled date cannot be in the past")

    data = maintenance_data.copy()
    data["scheduled_date"] = scheduled_date
    data["maintenance_number"] = (
        f"MNT-{datetime.now(timezone.utc):%Y%m%d}-{uuid4().hex[:8].upper()}"
    )
    data["status"] = "scheduled"
    data["reported_by"] = current_user_id

    try:
        record = create_maintenance(db, data)

        vehicle.status = "maintenance"

        db.commit()
        db.refresh(record)

        return record

    except Exception:
        db.rollback()
        raise


def list_maintenance_records(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    vehicle_id: int | None = None,
    status: str | None = None,
    maintenance_type: str | None = None,
    priority: str | None = None,
):
    filters = {
        "vehicle_id": vehicle_id,
        "status": status,
        "maintenance_type": maintenance_type,
        "priority": priority,
    }

    return {
        "total": count_maintenance(db, **filters),
        "maintenance_records": get_all_maintenance(
            db,
            skip=skip,
            limit=limit,
            **filters,
        ),
    }


def get_maintenance_details(db: Session, maintenance_id: int):
    record = get_maintenance_by_id(db, maintenance_id)

    if not record:
        raise ValueError("Maintenance record not found")

    return record


def update_existing_maintenance(
    db: Session,
    maintenance_id: int,
    update_data: dict,
):
    record = get_maintenance_details(db, maintenance_id)

    if record.status != "scheduled":
        raise ValueError(
            "Only scheduled maintenance records can be updated"
        )

    data = {
        key: value
        for key, value in update_data.items()
        if value is not None
    }

    if "scheduled_date" in data:
        scheduled_date = data["scheduled_date"]

        if scheduled_date.tzinfo is None:
            scheduled_date = scheduled_date.replace(tzinfo=timezone.utc)

        if scheduled_date < datetime.now(timezone.utc):
            raise ValueError("Scheduled date cannot be in the past")

        data["scheduled_date"] = scheduled_date

    try:
        updated = update_maintenance(db, record, data)
        db.commit()
        db.refresh(updated)

        return updated

    except Exception:
        db.rollback()
        raise


def update_maintenance_status(
    db: Session,
    maintenance_id: int,
    new_status: str,
    notes: str | None = None,
):
    record = get_maintenance_details(db, maintenance_id)

    allowed_transitions = {
        "scheduled": {"in_progress", "cancelled"},
        "in_progress": {"completed", "cancelled"},
        "completed": set(),
        "cancelled": set(),
    }

    if new_status not in allowed_transitions:
        raise ValueError("Invalid maintenance status")

    if new_status not in allowed_transitions[record.status]:
        raise ValueError(
            f"Cannot change maintenance status from {record.status} to {new_status}"
        )

    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == record.vehicle_id)
        .first()
    )

    if not vehicle:
        raise ValueError("Associated vehicle not found")

    try:
        now = datetime.now(timezone.utc)

        record.status = new_status

        if notes is not None:
            record.notes = notes

        if new_status == "in_progress":
            record.started_at = now
            vehicle.status = "maintenance"

        elif new_status in {"completed", "cancelled"}:
            if new_status == "completed":
                record.completed_at = now

            other_active = (
                db.query(VehicleMaintenance)
                .filter(
                    VehicleMaintenance.vehicle_id == vehicle.id,
                    VehicleMaintenance.id != record.id,
                    VehicleMaintenance.status.in_(
                        ["scheduled", "in_progress"]
                    ),
                )
                .first()
            )

            if not other_active:
                vehicle.status = "available"

        db.commit()
        db.refresh(record)

        return record

    except Exception:
        db.rollback()
        raise


def remove_maintenance(db: Session, maintenance_id: int):
    record = get_maintenance_details(db, maintenance_id)

    if record.status not in {"scheduled", "cancelled"}:
        raise ValueError(
            "Only scheduled or cancelled maintenance records can be deleted"
        )

    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == record.vehicle_id)
        .first()
    )

    try:
        delete_maintenance(db, record)

        if vehicle:
            other_active = (
                db.query(VehicleMaintenance)
                .filter(
                    VehicleMaintenance.vehicle_id == vehicle.id,
                    VehicleMaintenance.id != record.id,
                    VehicleMaintenance.status.in_(
                        ["scheduled", "in_progress"]
                    ),
                )
                .first()
            )

            if not other_active and vehicle.status == "maintenance":
                vehicle.status = "available"

        db.commit()

        return True

    except Exception:
        db.rollback()
        raise