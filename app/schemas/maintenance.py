from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import (
    MaintenanceType,
    MaintenanceStatus,
    MaintenancePriority,
)


class MaintenanceCreate(BaseModel):
    vehicle_id: int = Field(gt=0)
    maintenance_type: MaintenanceType
    priority: MaintenancePriority = MaintenancePriority.NORMAL
    description: str = Field(min_length=3)
    scheduled_date: datetime
    service_provider: str | None = Field(default=None, max_length=255)
    cost: float = Field(default=0, ge=0)
    odometer_reading: float | None = Field(default=None, ge=0)
    notes: str | None = None


class MaintenanceUpdate(BaseModel):
    maintenance_type: MaintenanceType | None = None
    priority: MaintenancePriority | None = None
    description: str | None = Field(default=None, min_length=3)
    scheduled_date: datetime | None = None
    service_provider: str | None = Field(default=None, max_length=255)
    cost: float | None = Field(default=None, ge=0)
    odometer_reading: float | None = Field(default=None, ge=0)
    notes: str | None = None


class MaintenanceStatusUpdate(BaseModel):
    status: MaintenanceStatus
    notes: str | None = None


class MaintenanceResponse(BaseModel):
    id: int
    maintenance_number: str
    vehicle_id: int
    maintenance_type: MaintenanceType
    priority: MaintenancePriority
    description: str
    scheduled_date: datetime
    started_at: datetime | None
    completed_at: datetime | None
    service_provider: str | None
    cost: float
    odometer_reading: float | None
    status: MaintenanceStatus
    reported_by: int
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MaintenanceListResponse(BaseModel):
    total: int
    maintenance_records: list[MaintenanceResponse]