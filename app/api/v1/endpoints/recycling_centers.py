from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User

from app.schemas.recycling_centers import (
    RecyclingCenterCreate,
    RecyclingCenterUpdate,
    RecyclingCenterStatusUpdate,
    RecyclingCenterResponse,
    RecyclingCenterListResponse,
)

from app.services.recycling_centers import (
    create_new_center,
    list_recycling_centers,
    get_recycling_center_details,
    update_existing_center,
    update_center_status,
    remove_recycling_center,
)


router = APIRouter(
    prefix="/recycling-centers",
    tags=["Recycling Center Management"],
)


@router.post(
    "/",
    response_model=RecyclingCenterResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_center_endpoint(
    payload: RecyclingCenterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return create_new_center(db, payload)


@router.get(
    "/",
    response_model=RecyclingCenterListResponse,
)
def get_centers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    center_type: str | None = None,
    center_status: str | None = None,
    city: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_recycling_centers(
        db=db,
        skip=skip,
        limit=limit,
        center_type=center_type,
        center_status=center_status,
        city=city,
    )


@router.get(
    "/{center_id}",
    response_model=RecyclingCenterResponse,
)
def get_center(
    center_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return get_recycling_center_details(db, center_id)


@router.patch(
    "/{center_id}",
    response_model=RecyclingCenterResponse,
)
def update_center_endpoint(
    center_id: int,
    payload: RecyclingCenterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_existing_center(
        db=db,
        center_id=center_id,
        payload=payload,
    )


@router.patch(
    "/{center_id}/status",
    response_model=RecyclingCenterResponse,
)
def change_center_status(
    center_id: int,
    payload: RecyclingCenterStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_center_status(
        db=db,
        center_id=center_id,
        new_status=payload.status,
    )


@router.delete(
    "/{center_id}",
)
def delete_center_endpoint(
    center_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return remove_recycling_center(db, center_id)