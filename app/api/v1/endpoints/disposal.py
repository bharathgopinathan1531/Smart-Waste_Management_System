from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User
from app.schemas.disposal import (
    DisposalCreate,
    DisposalUpdate,
    DisposalStatusUpdate,
    DisposalResponse,
    DisposalListResponse,
)
from app.services.disposal import (
    create_new_disposal,
    list_disposals,
    get_disposal_details,
    update_existing_disposal,
    update_disposal_status,
    remove_disposal,
)


router = APIRouter(
    prefix="/disposal",
    tags=["Waste Disposal Management"],
)


@router.post(
    "/",
    response_model=DisposalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_disposal_endpoint(
    payload: DisposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return create_new_disposal(
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
    response_model=DisposalListResponse,
)
def list_disposals_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    disposal_status: str | None = Query(None, alias="status"),
    waste_category_id: int | None = Query(None, gt=0),
    disposal_method: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_disposals(
        db,
        skip=skip,
        limit=limit,
        status=disposal_status,
        waste_category_id=waste_category_id,
        disposal_method=disposal_method,
    )


@router.get(
    "/{disposal_id}",
    response_model=DisposalResponse,
)
def get_disposal_endpoint(
    disposal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return get_disposal_details(db, disposal_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.patch(
    "/{disposal_id}",
    response_model=DisposalResponse,
)
def update_disposal_endpoint(
    disposal_id: int,
    payload: DisposalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_existing_disposal(
            db,
            disposal_id,
            payload.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.patch(
    "/{disposal_id}/status",
    response_model=DisposalResponse,
)
def update_disposal_status_endpoint(
    disposal_id: int,
    payload: DisposalStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_disposal_status(
            db,
            disposal_id,
            payload.status,
            current_user_id=current_user.id,
            notes=payload.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.delete(
    "/{disposal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_disposal_endpoint(
    disposal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        remove_disposal(db, disposal_id)
        return None
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )