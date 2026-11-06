from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import (
    PickupRequestStatus,
    PickupPriority,
)


class PickupRequestCreate(BaseModel):
    customer_id: int = Field(gt=0)
    location_id: int = Field(gt=0)
    waste_category_id: int = Field(gt=0)

    requested_date: date

    preferred_time: str | None = Field(
        default=None,
        max_length=50,
    )

    estimated_quantity: float = Field(
        gt=0,
        le=100000,
    )

    quantity_unit: str = Field(
        default="kg",
        min_length=1,
        max_length=20,
    )

    pickup_address: str = Field(
        min_length=5,
        max_length=1000,
    )

    priority: PickupPriority = PickupPriority.NORMAL

    special_instructions: str | None = None


class PickupRequestUpdate(BaseModel):
    requested_date: date | None = None

    preferred_time: str | None = Field(
        default=None,
        max_length=50,
    )

    estimated_quantity: float | None = Field(
        default=None,
        gt=0,
        le=100000,
    )

    quantity_unit: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    pickup_address: str | None = Field(
        default=None,
        min_length=5,
        max_length=1000,
    )

    priority: PickupPriority | None = None

    special_instructions: str | None = None


class PickupRequestStatusUpdate(BaseModel):
    status: PickupRequestStatus
    rejection_reason: str | None = None


class PickupRequestResponse(BaseModel):
    id: int
    request_number: str
    customer_id: int
    location_id: int
    waste_category_id: int
    requested_date: date
    preferred_time: str | None
    estimated_quantity: float
    quantity_unit: str
    pickup_address: str
    priority: PickupPriority
    status: PickupRequestStatus
    special_instructions: str | None
    rejection_reason: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PickupRequestListResponse(BaseModel):
    total: int
    requests: list[PickupRequestResponse]