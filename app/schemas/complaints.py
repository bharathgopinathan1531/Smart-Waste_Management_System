from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import (
    ComplaintCategory,
    ComplaintPriority,
    ComplaintStatus,
)


class ComplaintCreate(BaseModel):
    customer_id: int = Field(gt=0)
    category: ComplaintCategory
    priority: ComplaintPriority = ComplaintPriority.NORMAL
    subject: str = Field(min_length=5, max_length=255)
    description: str = Field(min_length=10)


class ComplaintUpdate(BaseModel):
    category: ComplaintCategory | None = None
    priority: ComplaintPriority | None = None
    subject: str | None = Field(default=None, min_length=5, max_length=255)
    description: str | None = Field(default=None, min_length=10)


class ComplaintAssignment(BaseModel):
    assigned_to: int = Field(gt=0)


class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus
    resolution_notes: str | None = None


class ComplaintResponse(BaseModel):
    id: int
    complaint_number: str
    customer_id: int
    category: ComplaintCategory
    priority: ComplaintPriority
    subject: str
    description: str
    status: ComplaintStatus
    assigned_to: int | None
    resolution_notes: str | None
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ComplaintListResponse(BaseModel):
    total: int
    complaints: list[ComplaintResponse]