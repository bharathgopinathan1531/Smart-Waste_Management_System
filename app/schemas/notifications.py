from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import (
    NotificationType,
    NotificationChannel,
    NotificationStatus,
)


class NotificationCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    message: str = Field(..., min_length=2)
    notification_type: NotificationType
    channel: NotificationChannel = NotificationChannel.IN_APP
    recipient_id: int = Field(..., gt=0)
    reference_type: str | None = None
    reference_id: int | None = Field(default=None, gt=0)


class NotificationUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    message: str | None = Field(default=None, min_length=2)
    status: NotificationStatus | None = None


class NotificationStatusUpdate(BaseModel):
    status: NotificationStatus


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    notification_type: NotificationType
    channel: NotificationChannel
    status: NotificationStatus
    recipient_id: int
    is_read: bool
    reference_type: str | None = None
    reference_id: int | None = None
    scheduled_at: datetime | None = None
    sent_at: datetime | None = None
    read_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationListResponse(BaseModel):
    total: int
    items: list[NotificationResponse] = Field(default_factory=list)