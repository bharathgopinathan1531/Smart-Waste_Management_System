from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import AssignmentStatus


class AssignmentCreate(BaseModel):
    pickup_request_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    driver_id: int = Field(gt=0)
    scheduled_at: datetime | None = None
    notes: str | None = None


class AssignmentUpdate(BaseModel):
    scheduled_at: datetime | None = None
    notes: str | None = None


class AssignmentStatusUpdate(BaseModel):
    status: AssignmentStatus
    notes: str | None = None


class AssignmentResponse(BaseModel):
    id: int
    assignment_number: str
    pickup_request_id: int
    vehicle_id: int
    driver_id: int
    supervisor_id: int | None
    assigned_at: datetime
    scheduled_at: datetime | None
    started_at: datetime | None
    completed_at: datetime | None
    status: AssignmentStatus
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssignmentListResponse(BaseModel):
    total: int
    assignments: list[AssignmentResponse]