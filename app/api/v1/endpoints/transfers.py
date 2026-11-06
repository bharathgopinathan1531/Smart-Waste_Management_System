from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User
from app.schemas.transfers import (
    WasteTransferCreate,
    WasteTransferUpdate,
    WasteTransferStatusUpdate,
    WasteTransferResponse,
    WasteTransferListResponse,
)
from app.services.transfers import (
    create_new_transfer,
    list_transfers,
    get_transfer_details,
    update_existing_transfer,
    update_transfer_status,
    remove_transfer,
)


router = APIRouter(
    prefix="/transfers",
    tags=["Waste Transfer Management"],
)


@router.post(
    "/",
    response_model=WasteTransferResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transfer_endpoint(
    payload: WasteTransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return create_new_transfer(
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
    response_model=WasteTransferListResponse,
)
def list_transfers_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    transfer_status: str | None = Query(None, alias="status"),
    recycling_center_id: int | None = Query(None, gt=0),
    collection_id: int | None = Query(None, gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_transfers(
        db,
        skip=skip,
        limit=limit,
        status=transfer_status,
        recycling_center_id=recycling_center_id,
        collection_id=collection_id,
    )


@router.get(
    "/{transfer_id}",
    response_model=WasteTransferResponse,
)
def get_transfer_endpoint(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return get_transfer_details(db, transfer_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.patch(
    "/{transfer_id}",
    response_model=WasteTransferResponse,
)
def update_transfer_endpoint(
    transfer_id: int,
    payload: WasteTransferUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_existing_transfer(
            db,
            transfer_id,
            payload.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.patch(
    "/{transfer_id}/status",
    response_model=WasteTransferResponse,
)
def update_transfer_status_endpoint(
    transfer_id: int,
    payload: WasteTransferStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        return update_transfer_status(
            db,
            transfer_id,
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
    "/{transfer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_transfer_endpoint(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    try:
        remove_transfer(db, transfer_id)
        return None
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )