from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User
from app.schemas.locations import (
    LocationCreate,
    LocationUpdate,
    LocationResponse,
    LocationListResponse,
)
from app.services.locations import (
    create_new_location,
    list_locations,
    get_location_details,
    update_existing_location,
    remove_location,
)
from app.utils.enums import LocationType, LocationStatus


router = APIRouter(
    prefix="/locations",
    tags=["Location Management"],
)


@router.post(
    "/",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_location(
    payload: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return create_new_location(db, payload)


@router.get(
    "/",
    response_model=LocationListResponse,
)
def get_locations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    location_type: LocationType | None = Query(default=None),
    location_status: LocationStatus | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_locations(
        db=db,
        skip=skip,
        limit=limit,
        location_type=location_type,
        location_status=location_status,
    )


@router.get(
    "/{location_id}",
    response_model=LocationResponse,
)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return get_location_details(db, location_id)


@router.patch(
    "/{location_id}",
    response_model=LocationResponse,
)
def update_location(
    location_id: int,
    payload: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_existing_location(
        db=db,
        location_id=location_id,
        payload=payload,
    )


@router.delete(
    "/{location_id}",
    status_code=status.HTTP_200_OK,
)
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    remove_location(db, location_id)

    return {
        "message": "Location deleted successfully",
        "location_id": location_id,
    }