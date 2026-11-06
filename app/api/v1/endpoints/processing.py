from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User
from app.schemas.processing import (
    ProcessingCreate,
    ProcessingUpdate,
    ProcessingStatusUpdate,
    ProcessingResponse,
    ProcessingListResponse,
)
from app.services.processing import (
    create_new_batch,
    list_batches,
    get_batch_details,
    update_existing_batch,
    update_batch_status,
    remove_batch,
)


router = APIRouter(
    prefix="/processing",
    tags=["Recycling Processing Management"],
)


@router.post(
    "/",
    response_model=ProcessingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_batch_endpoint(
    payload: ProcessingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return create_new_batch(
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
    response_model=ProcessingListResponse,
)
def list_batches_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    batch_status: str | None = Query(None, alias="status"),
    segregation_id: int | None = Query(None, gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_batches(
        db,
        skip=skip,
        limit=limit,
        status=batch_status,
        segregation_id=segregation_id,
    )


@router.get(
    "/{batch_id}",
    response_model=ProcessingResponse,
)
def get_batch_endpoint(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return get_batch_details(db, batch_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.patch(
    "/{batch_id}",
    response_model=ProcessingResponse,
)
def update_batch_endpoint(
    batch_id: int,
    payload: ProcessingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_existing_batch(
            db,
            batch_id,
            payload.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.patch(
    "/{batch_id}/status",
    response_model=ProcessingResponse,
)
def update_batch_status_endpoint(
    batch_id: int,
    payload: ProcessingStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_batch_status(
            db,
            batch_id,
            payload.status,
            notes=payload.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.delete(
    "/{batch_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_batch_endpoint(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        remove_batch(db, batch_id)
        return None
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )