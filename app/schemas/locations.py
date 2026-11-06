from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import LocationType, LocationStatus


class LocationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    code: str = Field(min_length=2, max_length=50)
    location_type: LocationType
    description: str | None = None
    address: str | None = Field(default=None, max_length=255)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    parent_id: int | None = Field(default=None, gt=0)


class LocationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    address: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    state: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    parent_id: int | None = Field(default=None, gt=0)
    status: LocationStatus | None = None


class LocationResponse(BaseModel):
    id: int
    name: str
    code: str
    location_type: LocationType
    description: str | None
    address: str | None
    city: str
    state: str
    postal_code: str | None
    latitude: float | None
    longitude: float | None
    parent_id: int | None
    status: LocationStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LocationListResponse(BaseModel):
    total: int
    locations: list[LocationResponse]