from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.vehicle import (
    get_vehicle_by_id,
    get_vehicle_by_registration,
    get_all_vehicles,
    count_vehicles,
    create_vehicle,
    update_vehicle,
    delete_vehicle,
)
from app.schemas.vehicles import VehicleCreate, VehicleUpdate
from app.utils.enums import VehicleStatus


def create_new_vehicle(db: Session, payload: VehicleCreate):
    registration_number = payload.registration_number.strip().upper()

    existing_vehicle = get_vehicle_by_registration(
        db,
        registration_number,
    )

    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vehicle registration number already exists",
        )

    vehicle_data = payload.model_dump()

    vehicle_data["registration_number"] = registration_number
    vehicle_data["vehicle_type"] = payload.vehicle_type.value
    vehicle_data["fuel_type"] = payload.fuel_type.value
    vehicle_data["status"] = VehicleStatus.AVAILABLE.value

    if vehicle_data.get("vehicle_name"):
        vehicle_data["vehicle_name"] = vehicle_data["vehicle_name"].strip()

    if vehicle_data.get("manufacturer"):
        vehicle_data["manufacturer"] = vehicle_data["manufacturer"].strip()

    if vehicle_data.get("model_name"):
        vehicle_data["model_name"] = vehicle_data["model_name"].strip()

    return create_vehicle(db, vehicle_data)


def list_vehicles(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    vehicle_status: VehicleStatus | None = None,
    vehicle_type=None,
    fuel_type=None,
    search: str | None = None,
):
    status_value = vehicle_status.value if vehicle_status else None
    type_value = vehicle_type.value if vehicle_type else None
    fuel_value = fuel_type.value if fuel_type else None

    vehicles = get_all_vehicles(
        db=db,
        skip=skip,
        limit=limit,
        vehicle_status=status_value,
        vehicle_type=type_value,
        fuel_type=fuel_value,
        search=search,
    )

    total = count_vehicles(
        db=db,
        vehicle_status=status_value,
        vehicle_type=type_value,
        fuel_type=fuel_value,
        search=search,
    )

    return {
        "total": total,
        "vehicles": vehicles,
    }


def get_vehicle_details(db: Session, vehicle_id: int):
    vehicle = get_vehicle_by_id(db, vehicle_id)

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )

    return vehicle


def update_existing_vehicle(
    db: Session,
    vehicle_id: int,
    payload: VehicleUpdate,
):
    vehicle = get_vehicle_details(db, vehicle_id)

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update fields provided",
        )

    if "vehicle_type" in update_data and update_data["vehicle_type"]:
        update_data["vehicle_type"] = update_data["vehicle_type"].value

    if "fuel_type" in update_data and update_data["fuel_type"]:
        update_data["fuel_type"] = update_data["fuel_type"].value

    for field in ("vehicle_name", "manufacturer", "model_name"):
        if field in update_data and update_data[field] is not None:
            update_data[field] = update_data[field].strip()

    if "capacity_kg" in update_data and update_data["capacity_kg"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Vehicle capacity must be greater than zero",
        )

    return update_vehicle(db, vehicle, update_data)


def update_vehicle_status(
    db: Session,
    vehicle_id: int,
    new_status: VehicleStatus,
):
    vehicle = get_vehicle_details(db, vehicle_id)

    if (
        vehicle.status == VehicleStatus.ON_ROUTE.value
        and new_status == VehicleStatus.MAINTENANCE
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An on-route vehicle cannot be moved to maintenance",
        )

    if (
        vehicle.status == VehicleStatus.ON_ROUTE.value
        and new_status == VehicleStatus.INACTIVE
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An on-route vehicle cannot be deactivated",
        )

    return update_vehicle(
        db,
        vehicle,
        {"status": new_status.value},
    )


def remove_vehicle(db: Session, vehicle_id: int):
    vehicle = get_vehicle_details(db, vehicle_id)

    if vehicle.status == VehicleStatus.ON_ROUTE.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a vehicle that is currently on route",
        )

    delete_vehicle(db, vehicle)

    return {
        "message": "Vehicle deleted successfully",
        "vehicle_id": vehicle_id,
    }