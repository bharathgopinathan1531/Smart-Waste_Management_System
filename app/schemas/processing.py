from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProcessingCreate(BaseModel):
    segregation_id: int = Field(gt=0)
    processing_method: str = "sorting"
    input_quantity: float = Field(gt=0)
    quantity_unit: str = "kg"
    notes: str | None = None

    @field_validator("processing_method")
    @classmethod
    def validate_method(cls, value: str) -> str:
        value = value.strip().lower()
        allowed = {
            "shredding",
            "compacting",
            "melting",
            "composting",
            "sorting",
            "other",
        }
        if value not in allowed:
            raise ValueError("Invalid processing method")
        return value

    @field_validator("quantity_unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        value = value.strip().lower()
        if not value:
            raise ValueError("Quantity unit cannot be empty")
        return value


class ProcessingUpdate(BaseModel):
    processing_method: str | None = None
    input_quantity: float | None = Field(default=None, gt=0)
    recovered_quantity: float | None = Field(default=None, ge=0)
    rejected_quantity: float | None = Field(default=None, ge=0)
    quantity_unit: str | None = None
    notes: str | None = None


class ProcessingStatusUpdate(BaseModel):
    status: str
    notes: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"pending", "in_progress", "completed", "cancelled"}:
            raise ValueError("Invalid processing status")
        return value


class ProcessingResponse(BaseModel):
    id: int
    batch_number: str
    segregation_id: int
    processing_method: str
    input_quantity: float
    recovered_quantity: float
    rejected_quantity: float
    quantity_unit: str
    recovery_rate: float
    status: str
    processed_by: int | None
    started_at: datetime | None
    completed_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProcessingListResponse(BaseModel):
    total: int
    batches: list[ProcessingResponse]