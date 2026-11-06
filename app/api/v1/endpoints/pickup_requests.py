from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User

from app.schemas.pickup_requests import (
    PickupRequestCreate,
    PickupRequestUpdate,
    PickupRequestStatusUpdate,
    PickupRequestResponse,
    PickupRequestListResponse,
)

from app.utils.enums import PickupRequestStatus, PickupPriority

from app.services.pickup_requests import (
    create_new_request,
    list_pickup_requests,
    get_request_details,
    update_existing_request,
    update_request_status,
    cancel_pickup_request,
    remove_pickup_request,
)


router = APIRouter(
    prefix="/pickup-requests",
    tags=["Pickup Request Management"],
)


@router.post(
    "/",
    response_model=PickupRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_pickup_request(
    payload: PickupRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return create_new_request(db, payload)


@router.get(
    "/",
    response_model=PickupRequestListResponse,
)
def get_pickup_requests(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    request_status: PickupRequestStatus | None = Query(default=None),
    priority: PickupPriority | None = Query(default=None),
    customer_id: int | None = Query(default=None, gt=0),
    location_id: int | None = Query(default=None, gt=0),
    search: str | None = Query(default=None, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_pickup_requests(
        db=db,
        skip=skip,
        limit=limit,
        request_status=request_status,
        priority=priority,
        customer_id=customer_id,
        location_id=location_id,
        search=search,
    )


@router.get(
    "/{request_id}",
    response_model=PickupRequestResponse,
)
def get_pickup_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return get_request_details(db, request_id)


@router.patch(
    "/{request_id}",
    response_model=PickupRequestResponse,
)
def update_pickup_request(
    request_id: int,
    payload: PickupRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_existing_request(
        db=db,
        request_id=request_id,
        payload=payload,
    )


@router.patch(
    "/{request_id}/status",
    response_model=PickupRequestResponse,
)
def change_pickup_request_status(
    request_id: int,
    payload: PickupRequestStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_request_status(
        db=db,
        request_id=request_id,
        new_status=payload.status,
        rejection_reason=payload.rejection_reason,
    )


@router.patch(
    "/{request_id}/cancel",
    response_model=PickupRequestResponse,
)
def cancel_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return cancel_pickup_request(db, request_id)


@router.delete(
    "/{request_id}",
)
def delete_pickup_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return remove_pickup_request(db, request_id)