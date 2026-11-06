from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SQLAlchemyEnum,
    Boolean,
)
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.utils.enums import (
    NotificationType,
    NotificationChannel,
    NotificationStatus,
)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)

    notification_type = Column(
        SQLAlchemyEnum(NotificationType),
        nullable=False,
    )

    channel = Column(
        SQLAlchemyEnum(NotificationChannel),
        default=NotificationChannel.IN_APP,
        nullable=False,
    )

    status = Column(
        SQLAlchemyEnum(NotificationStatus),
        default=NotificationStatus.UNREAD,
        nullable=False,
    )

    recipient_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    is_read = Column(Boolean, default=False, nullable=False)

    reference_type = Column(String(100), nullable=True)
    reference_id = Column(Integer, nullable=True)

    scheduled_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    recipient = relationship("User")