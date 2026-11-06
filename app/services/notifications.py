
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User
from app.repositories.notification import (
    get_notification_by_id,
    get_all_notifications,
    count_notifications,
    create_notification,
    delete_notification,
)
from app.utils.enums import NotificationStatus, NotificationChannel


def _normalize_status(value):
    """Convert enum or string status into a consistent string."""
    return value.value if hasattr(value, "value") else str(value)


def create_new_notification(db: Session, data: dict):
    recipient_id = data.get("recipient_id")

    if not recipient_id:
        raise ValueError("Notification recipient is required")

    recipient = db.query(User).filter(
        User.id == recipient_id
    ).first()

    if not recipient:
        raise ValueError("Notification recipient not found")

    if not recipient.is_active:
        raise ValueError("Notification recipient is inactive")

    notification_data = dict(data)

    channel = notification_data.get(
        "channel",
        NotificationChannel.IN_APP,
    )

    if not isinstance(channel, NotificationChannel):
        channel = NotificationChannel(channel)

    notification_data["channel"] = channel
    notification_data["status"] = NotificationStatus.UNREAD
    notification_data["is_read"] = False
    notification_data["read_at"] = None

    if channel == NotificationChannel.IN_APP:
        notification_data["sent_at"] = datetime.now(timezone.utc)
    else:
        notification_data["sent_at"] = None

    try:
        notification = create_notification(db, notification_data)
        db.commit()
        db.refresh(notification)
        return notification
    except Exception:
        db.rollback()
        raise


def list_notifications(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    recipient_id: int = None,
    status=None,
    notification_type=None,
):
    if status is not None:
        status = _normalize_status(status)

    if notification_type is not None:
        notification_type = _normalize_status(notification_type)

    notifications = get_all_notifications(
        db=db,
        skip=skip,
        limit=limit,
        recipient_id=recipient_id,
        status=status,
        notification_type=notification_type,
    )

    total = count_notifications(
        db=db,
        recipient_id=recipient_id,
        status=status,
        notification_type=notification_type,
    )

    return {
        "items": notifications,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


def get_notification_details(db: Session, notification_id: int):
    notification = get_notification_by_id(db, notification_id)

    if not notification:
        raise ValueError("Notification not found")

    return notification


def mark_notification_read(
    db: Session,
    notification_id: int,
    recipient_id: int,
):
    notification = get_notification_by_id(db, notification_id)

    if not notification:
        raise ValueError("Notification not found")

    if notification.recipient_id != recipient_id:
        raise ValueError(
            "You cannot modify another user's notification"
        )

    current_status = _normalize_status(notification.status)

    if current_status == NotificationStatus.ARCHIVED.value:
        raise ValueError(
            "Archived notifications cannot be marked as read"
        )

    try:
        notification.status = NotificationStatus.READ
        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(notification)
        return notification
    except Exception:
        db.rollback()
        raise


def update_notification_status(
    db: Session,
    notification_id: int,
    recipient_id: int,
    status: str,
):
    notification = get_notification_by_id(db, notification_id)

    if not notification:
        raise ValueError("Notification not found")

    if notification.recipient_id != recipient_id:
        raise ValueError(
            "You cannot modify another user's notification"
        )

    current_status = _normalize_status(notification.status)
    new_status = _normalize_status(status)

    if current_status == NotificationStatus.ARCHIVED.value:
        raise ValueError(
            "Archived notifications cannot be updated"
        )

    allowed_statuses = {
        NotificationStatus.READ.value,
        NotificationStatus.ARCHIVED.value,
    }

    if new_status not in allowed_statuses:
        raise ValueError(
            "Only read or archived status is allowed"
        )

    try:
        notification.status = NotificationStatus(new_status)
        notification.is_read = (
            new_status == NotificationStatus.READ.value
        )

        if notification.is_read:
            notification.read_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(notification)
        return notification
    except Exception:
        db.rollback()
        raise


def remove_notification(
    db: Session,
    notification_id: int,
    recipient_id: int,
):
    notification = get_notification_by_id(db, notification_id)

    if not notification:
        raise ValueError("Notification not found")

    if notification.recipient_id != recipient_id:
        raise ValueError(
            "You cannot delete another user's notification"
        )

    try:
        delete_notification(db, notification)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
