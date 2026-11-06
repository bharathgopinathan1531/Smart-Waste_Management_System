from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CollectionCreate(BaseModel):
    assignment_id: int = Field(gt=0)
    collected_quantity: float = Field(gt=0)
    quantity_unit: str = Field(default="kg", min_length=1, max_length=20)
    collection_address: str | None = Field(default=None, max_length=500)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    collection_started_at: datetime | None = None
    proof_image_url: str | None = Field(default=None, max_length=500)
    notes: str | None = None

    @field_validator("quantity_unit")
    @classmethod
    def normalize_quantity_unit(cls, value: str) -> str:
        return value.strip().lower()


class CollectionUpdate(BaseModel):
    collected_quantity: float | None = Field(default=None, gt=0)
    quantity_unit: str | None = Field(default=None, min_length=1, max_length=20)
    collection_address: str | None = Field(default=None, max_length=500)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    proof_image_url: str | None = Field(default=None, max_length=500)
    notes: str | None = None


class CollectionResponse(BaseModel):
    id: int
    collection_number: str
    assignment_id: int
    collected_quantity: float
    quantity_unit: str
    collection_address: str | None
    latitude: float | None
    longitude: float | None
    collection_started_at: datetime | None
    collection_completed_at: datetime
    proof_image_url: str | None
    notes: str | None
    recorded_by: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CollectionListResponse(BaseModel):
    total: int
    collections: list[CollectionResponse]