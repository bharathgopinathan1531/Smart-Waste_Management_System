from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
    MaintenanceStatusUpdate,
    MaintenanceResponse,
    MaintenanceListResponse,
)
from app.services.maintenance import (
    create_new_maintenance,
    list_maintenance_records,
    get_maintenance_details,
    update_existing_maintenance,
    update_maintenance_status,
    remove_maintenance,
)


router = APIRouter(
    prefix="/maintenance",
    tags=["Vehicle Maintenance Management"],
)


@router.post(
    "/",
    response_model=MaintenanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_maintenance_endpoint(
    payload: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return create_new_maintenance(
            db,
            payload.model_dump(),
            current_user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/",
    response_model=MaintenanceListResponse,
)
def list_maintenance_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    vehicle_id: int | None = Query(None, gt=0),
    maintenance_status: str | None = Query(None, alias="status"),
    maintenance_type: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_maintenance_records(
        db,
        skip=skip,
        limit=limit,
        vehicle_id=vehicle_id,
        status=maintenance_status,
        maintenance_type=maintenance_type,
        priority=priority,
    )


@router.get(
    "/{maintenance_id}",
    response_model=MaintenanceResponse,
)
def get_maintenance_endpoint(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return get_maintenance_details(db, maintenance_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.patch(
    "/{maintenance_id}",
    response_model=MaintenanceResponse,
)
def update_maintenance_endpoint(
    maintenance_id: int,
    payload: MaintenanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_existing_maintenance(
            db,
            maintenance_id,
            payload.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.patch(
    "/{maintenance_id}/status",
    response_model=MaintenanceResponse,
)
def update_maintenance_status_endpoint(
    maintenance_id: int,
    payload: MaintenanceStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_maintenance_status(
            db,
            maintenance_id,
            payload.status,
            notes=payload.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.delete(
    "/{maintenance_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_maintenance_endpoint(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        remove_maintenance(db, maintenance_id)
        return None
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )