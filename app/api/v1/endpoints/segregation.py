from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User
from app.schemas.segregation import (
    SegregationCreate,
    SegregationUpdate,
    SegregationStatusUpdate,
    SegregationResponse,
    SegregationListResponse,
)
from app.services.segregation import (
    create_new_segregation,
    list_segregations,
    get_segregation_details,
    update_existing_segregation,
    update_segregation_status,
    remove_segregation,
)


router = APIRouter(
    prefix="/segregation",
    tags=["Waste Segregation Management"],
)


@router.post(
    "/",
    response_model=SegregationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_segregation_endpoint(
    payload: SegregationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return create_new_segregation(
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
    response_model=SegregationListResponse,
)
def list_segregations_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    segregation_status: str | None = Query(None, alias="status"),
    transfer_id: int | None = Query(None, gt=0),
    waste_category_id: int | None = Query(None, gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_segregations(
        db,
        skip=skip,
        limit=limit,
        status=segregation_status,
        transfer_id=transfer_id,
        waste_category_id=waste_category_id,
    )


@router.get(
    "/{segregation_id}",
    response_model=SegregationResponse,
)
def get_segregation_endpoint(
    segregation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return get_segregation_details(db, segregation_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.patch(
    "/{segregation_id}",
    response_model=SegregationResponse,
)
def update_segregation_endpoint(
    segregation_id: int,
    payload: SegregationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_existing_segregation(
            db,
            segregation_id,
            payload.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.patch(
    "/{segregation_id}/status",
    response_model=SegregationResponse,
)
def update_segregation_status_endpoint(
    segregation_id: int,
    payload: SegregationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_segregation_status(
            db,
            segregation_id,
            payload.status,
            notes=payload.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.delete(
    "/{segregation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_segregation_endpoint(
    segregation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        remove_segregation(db, segregation_id)
        return None
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )