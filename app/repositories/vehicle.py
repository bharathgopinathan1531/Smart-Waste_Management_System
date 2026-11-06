from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle


def get_vehicle_by_id(db: Session, vehicle_id: int):
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def get_vehicle_by_registration(db: Session, registration_number: str):
    return (
        db.query(Vehicle)
        .filter(Vehicle.registration_number == registration_number)
        .first()
    )


def get_all_vehicles(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    vehicle_status: str | None = None,
    vehicle_type: str | None = None,
    fuel_type: str | None = None,
    search: str | None = None,
):
    query = db.query(Vehicle)

    if vehicle_status:
        query = query.filter(Vehicle.status == vehicle_status)

    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type)

    if fuel_type:
        query = query.filter(Vehicle.fuel_type == fuel_type)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Vehicle.registration_number.ilike(search_term),
                Vehicle.vehicle_name.ilike(search_term),
                Vehicle.manufacturer.ilike(search_term),
                Vehicle.model_name.ilike(search_term),
            )
        )

    return (
        query.order_by(Vehicle.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_vehicles(
    db: Session,
    vehicle_status: str | None = None,
    vehicle_type: str | None = None,
    fuel_type: str | None = None,
    search: str | None = None,
):
    query = db.query(Vehicle)

    if vehicle_status:
        query = query.filter(Vehicle.status == vehicle_status)

    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type)

    if fuel_type:
        query = query.filter(Vehicle.fuel_type == fuel_type)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Vehicle.registration_number.ilike(search_term),
                Vehicle.vehicle_name.ilike(search_term),
                Vehicle.manufacturer.ilike(search_term),
                Vehicle.model_name.ilike(search_term),
            )
        )

    return query.count()


def create_vehicle(db: Session, vehicle_data: dict):
    try:
        vehicle = Vehicle(**vehicle_data)
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return vehicle
    except Exception:
        db.rollback()
        raise


def update_vehicle(db: Session, vehicle: Vehicle, update_data: dict):
    try:
        for key, value in update_data.items():
            setattr(vehicle, key, value)

        db.commit()
        db.refresh(vehicle)
        return vehicle
    except Exception:
        db.rollback()
        raise


def delete_vehicle(db: Session, vehicle: Vehicle):
    try:
        db.delete(vehicle)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise