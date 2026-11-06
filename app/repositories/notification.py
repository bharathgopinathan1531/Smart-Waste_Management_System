from sqlalchemy.orm import Session

from app.models.notification import Notification


def get_notification_by_id(db: Session, notification_id: int):
    return (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )


def get_all_notifications(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    recipient_id: int = None,
    status=None,
    notification_type=None,
):
    query = db.query(Notification)

    if recipient_id is not None:
        query = query.filter(Notification.recipient_id == recipient_id)

    if status is not None:
        query = query.filter(Notification.status == status)

    if notification_type is not None:
        query = query.filter(
            Notification.notification_type == notification_type
        )

    return (
        query.order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_notifications(
    db: Session,
    recipient_id: int = None,
    status=None,
    notification_type=None,
):
    query = db.query(Notification)

    if recipient_id is not None:
        query = query.filter(Notification.recipient_id == recipient_id)

    if status is not None:
        query = query.filter(Notification.status == status)

    if notification_type is not None:
        query = query.filter(
            Notification.notification_type == notification_type
        )

    return query.count()


def create_notification(db: Session, notification_data: dict):
    notification = Notification(**notification_data)
    db.add(notification)
    db.flush()
    return notification


def update_notification(
    db: Session,
    notification: Notification,
    update_data: dict,
):
    for key, value in update_data.items():
        if hasattr(notification, key):
            setattr(notification, key, value)

    db.flush()
    return notification


def delete_notification(db: Session, notification: Notification):
    db.delete(notification)
    db.flush()
    return True