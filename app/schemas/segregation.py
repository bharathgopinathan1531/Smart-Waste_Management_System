from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SegregationCreate(BaseModel):
    transfer_id: int = Field(gt=0)
    waste_category_id: int = Field(gt=0)
    segregated_quantity: float = Field(gt=0)
    quantity_unit: str = "kg"
    quality: str = "good"
    notes: str | None = None

    @field_validator("quantity_unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        value = value.strip().lower()
        if not value:
            raise ValueError("Quantity unit cannot be empty")
        return value

    @field_validator("quality")
    @classmethod
    def validate_quality(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"excellent", "good", "average", "poor"}:
            raise ValueError("Invalid segregation quality")
        return value


class SegregationUpdate(BaseModel):
    segregated_quantity: float | None = Field(default=None, gt=0)
    quantity_unit: str | None = None
    quality: str | None = None
    notes: str | None = None


class SegregationStatusUpdate(BaseModel):
    status: str
    notes: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"pending", "in_progress", "completed", "cancelled"}:
            raise ValueError("Invalid segregation status")
        return value


class SegregationResponse(BaseModel):
    id: int
    segregation_number: str
    transfer_id: int
    waste_category_id: int
    segregated_quantity: float
    quantity_unit: str
    quality: str
    status: str
    segregated_by: int | None
    started_at: datetime | None
    completed_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SegregationListResponse(BaseModel):
    total: int
    segregations: list[SegregationResponse]