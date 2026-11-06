from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WasteTransferCreate(BaseModel):
    collection_id: int = Field(gt=0)
    recycling_center_id: int = Field(gt=0)
    transferred_quantity: float = Field(gt=0)
    quantity_unit: str = "kg"
    transfer_type: str = "direct"
    vehicle_id: int | None = Field(default=None, gt=0)
    notes: str | None = None

    @field_validator("quantity_unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        value = value.strip().lower()
        if not value:
            raise ValueError("Quantity unit cannot be empty")
        return value

    @field_validator("transfer_type")
    @classmethod
    def validate_transfer_type(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"direct", "intermediate"}:
            raise ValueError("Invalid transfer type")
        return value


class WasteTransferUpdate(BaseModel):
    transferred_quantity: float | None = Field(default=None, gt=0)
    quantity_unit: str | None = None
    transfer_type: str | None = None
    vehicle_id: int | None = Field(default=None, gt=0)
    notes: str | None = None


class WasteTransferStatusUpdate(BaseModel):
    status: str
    notes: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"pending", "in_transit", "received", "cancelled"}:
            raise ValueError("Invalid waste transfer status")
        return value


class WasteTransferResponse(BaseModel):
    id: int
    transfer_number: str
    collection_id: int
    recycling_center_id: int
    transferred_quantity: float
    quantity_unit: str
    transfer_type: str
    status: str
    vehicle_id: int | None
    transferred_by: int | None
    received_by: int | None
    transferred_at: datetime | None
    received_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WasteTransferListResponse(BaseModel):
    total: int
    transfers: list[WasteTransferResponse]