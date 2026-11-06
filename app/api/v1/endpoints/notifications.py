from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import require_management

from app.schemas.notifications import (
    NotificationCreate,
    NotificationStatusUpdate,
    NotificationResponse,
    NotificationListResponse,
)

from app.services.notifications import (
    create_new_notification,
    list_notifications,
    get_notification_details,
    mark_notification_read,
    update_notification_status,
    remove_notification,
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notification Management"],
)


@router.post(
    "/",
    response_model=NotificationResponse,
    dependencies=[Depends(require_management())],
)
def create_notification_endpoint(
    data: NotificationCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_new_notification(db, data.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get(
    "/my",
    response_model=NotificationListResponse,
)
def get_my_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_notifications(
        db,
        skip=skip,
        limit=limit,
        recipient_id=current_user.id,
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def get_notification_endpoint(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        notification = get_notification_details(db, notification_id)

        if notification.recipient_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You cannot access another user's notification",
            )

        return notification
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_notification_read_endpoint(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return mark_notification_read(
            db,
            notification_id,
            current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch(
    "/{notification_id}/status",
    response_model=NotificationResponse,
)
def update_notification_status_endpoint(
    notification_id: int,
    data: NotificationStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return update_notification_status(
            db,
            notification_id,
            current_user.id,
            data.status.value,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete(
    "/{notification_id}",
)
def delete_notification_endpoint(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        remove_notification(
            db,
            notification_id,
            current_user.id,
        )

        return {"message": "Notification deleted successfully"}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))