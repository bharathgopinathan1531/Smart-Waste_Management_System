from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import DisposalMethod, DisposalStatus


class DisposalCreate(BaseModel):
    processing_batch_id: int | None = Field(default=None, gt=0)
    transfer_id: int | None = Field(default=None, gt=0)
    waste_category_id: int = Field(gt=0)
    disposal_method: DisposalMethod
    quantity: float = Field(gt=0)
    quantity_unit: str = Field(default="kg", min_length=1, max_length=20)
    disposal_location: str = Field(min_length=2, max_length=255)
    disposal_date: datetime
    notes: str | None = None


class DisposalUpdate(BaseModel):
    disposal_method: DisposalMethod | None = None
    quantity: float | None = Field(default=None, gt=0)
    quantity_unit: str | None = Field(
        default=None, min_length=1, max_length=20
    )
    disposal_location: str | None = Field(
        default=None, min_length=2, max_length=255
    )
    disposal_date: datetime | None = None
    notes: str | None = None


class DisposalStatusUpdate(BaseModel):
    status: DisposalStatus
    notes: str | None = None


class DisposalResponse(BaseModel):
    id: int
    disposal_number: str
    processing_batch_id: int | None
    transfer_id: int | None
    waste_category_id: int
    disposal_method: DisposalMethod
    quantity: float
    quantity_unit: str
    disposal_location: str
    disposal_date: datetime
    status: DisposalStatus
    recorded_by: int
    approved_by: int | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DisposalListResponse(BaseModel):
    total: int
    disposals: list[DisposalResponse]