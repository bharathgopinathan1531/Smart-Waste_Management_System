from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User

from app.schemas.vehicles import (
    VehicleCreate,
    VehicleUpdate,
    VehicleStatusUpdate,
    VehicleResponse,
    VehicleListResponse,
)

from app.utils.enums import VehicleType, VehicleStatus, FuelType

from app.services.vehicles import (
    create_new_vehicle,
    list_vehicles,
    get_vehicle_details,
    update_existing_vehicle,
    update_vehicle_status,
    remove_vehicle,
)


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicle Management"],
)


@router.post(
    "/",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vehicle_endpoint(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return create_new_vehicle(db, payload)


@router.get(
    "/",
    response_model=VehicleListResponse,
)
def get_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    vehicle_status: VehicleStatus | None = Query(None),
    vehicle_type: VehicleType | None = Query(None),
    fuel_type: FuelType | None = Query(None),
    search: str | None = Query(None, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_vehicles(
        db=db,
        skip=skip,
        limit=limit,
        vehicle_status=vehicle_status,
        vehicle_type=vehicle_type,
        fuel_type=fuel_type,
        search=search,
    )


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return get_vehicle_details(db, vehicle_id)


@router.patch(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def update_vehicle_endpoint(
    vehicle_id: int,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_existing_vehicle(
        db=db,
        vehicle_id=vehicle_id,
        payload=payload,
    )


@router.patch(
    "/{vehicle_id}/status",
    response_model=VehicleResponse,
)
def change_vehicle_status(
    vehicle_id: int,
    payload: VehicleStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_vehicle_status(
        db=db,
        vehicle_id=vehicle_id,
        new_status=payload.status,
    )


@router.delete(
    "/{vehicle_id}",
)
def delete_vehicle_endpoint(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return remove_vehicle(db, vehicle_id)