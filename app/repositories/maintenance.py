from sqlalchemy.orm import Session

from app.models.maintenance import VehicleMaintenance


def get_maintenance_by_id(db: Session, maintenance_id: int):
    return (
        db.query(VehicleMaintenance)
        .filter(VehicleMaintenance.id == maintenance_id)
        .first()
    )


def get_maintenance_by_number(db: Session, maintenance_number: str):
    return (
        db.query(VehicleMaintenance)
        .filter(
            VehicleMaintenance.maintenance_number == maintenance_number
        )
        .first()
    )


def get_all_maintenance(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    vehicle_id: int | None = None,
    status: str | None = None,
    maintenance_type: str | None = None,
    priority: str | None = None,
):
    query = db.query(VehicleMaintenance)

    if vehicle_id is not None:
        query = query.filter(
            VehicleMaintenance.vehicle_id == vehicle_id
        )

    if status:
        query = query.filter(VehicleMaintenance.status == status)

    if maintenance_type:
        query = query.filter(
            VehicleMaintenance.maintenance_type == maintenance_type
        )

    if priority:
        query = query.filter(VehicleMaintenance.priority == priority)

    return (
        query.order_by(VehicleMaintenance.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_maintenance(
    db: Session,
    vehicle_id: int | None = None,
    status: str | None = None,
    maintenance_type: str | None = None,
    priority: str | None = None,
):
    query = db.query(VehicleMaintenance)

    if vehicle_id is not None:
        query = query.filter(
            VehicleMaintenance.vehicle_id == vehicle_id
        )

    if status:
        query = query.filter(VehicleMaintenance.status == status)

    if maintenance_type:
        query = query.filter(
            VehicleMaintenance.maintenance_type == maintenance_type
        )

    if priority:
        query = query.filter(VehicleMaintenance.priority == priority)

    return query.count()


def create_maintenance(db: Session, maintenance_data: dict):
    record = VehicleMaintenance(**maintenance_data)

    db.add(record)
    db.flush()

    return record


def update_maintenance(
    db: Session,
    record: VehicleMaintenance,
    update_data: dict,
):
    for key, value in update_data.items():
        if hasattr(record, key):
            setattr(record, key, value)

    db.flush()

    return record


def delete_maintenance(db: Session, record: VehicleMaintenance):
    db.delete(record)
    db.flush()

    return True