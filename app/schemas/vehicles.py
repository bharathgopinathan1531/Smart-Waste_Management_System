from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import VehicleType, VehicleStatus, FuelType


class VehicleCreate(BaseModel):
    registration_number: str = Field(
        min_length=3,
        max_length=30,
    )

    vehicle_name: str = Field(
        min_length=2,
        max_length=100,
    )

    vehicle_type: VehicleType

    capacity_kg: float = Field(
        gt=0,
        le=100000,
    )

    fuel_type: FuelType

    manufacturer: str | None = Field(
        default=None,
        max_length=100,
    )

    model_name: str | None = Field(
        default=None,
        max_length=100,
    )

    manufacturing_year: int | None = Field(
        default=None,
        ge=1950,
        le=2100,
    )

    current_location: str | None = Field(
        default=None,
        max_length=255,
    )

    notes: str | None = None


class VehicleUpdate(BaseModel):
    vehicle_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    vehicle_type: VehicleType | None = None

    capacity_kg: float | None = Field(
        default=None,
        gt=0,
        le=100000,
    )

    fuel_type: FuelType | None = None

    manufacturer: str | None = Field(
        default=None,
        max_length=100,
    )

    model_name: str | None = Field(
        default=None,
        max_length=100,
    )

    manufacturing_year: int | None = Field(
        default=None,
        ge=1950,
        le=2100,
    )

    current_location: str | None = Field(
        default=None,
        max_length=255,
    )

    notes: str | None = None


class VehicleStatusUpdate(BaseModel):
    status: VehicleStatus


class VehicleResponse(BaseModel):
    id: int
    registration_number: str
    vehicle_name: str
    vehicle_type: VehicleType
    capacity_kg: float
    fuel_type: FuelType
    manufacturer: str | None
    model_name: str | None
    manufacturing_year: int | None
    status: VehicleStatus
    current_location: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VehicleListResponse(BaseModel):
    total: int
    vehicles: list[VehicleResponse]