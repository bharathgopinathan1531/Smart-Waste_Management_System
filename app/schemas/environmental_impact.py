from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import EnvironmentalImpactStatus


class EnvironmentalImpactBase(BaseModel):
    start_date: date
    end_date: date


class EnvironmentalImpactCreate(EnvironmentalImpactBase):
    pass


class EnvironmentalImpactStatusUpdate(BaseModel):
    status: EnvironmentalImpactStatus
    notes: str | None = None


class EnvironmentalImpactResponse(EnvironmentalImpactBase):
    id: int
    report_number: str

    total_waste_collected_kg: float
    total_waste_recycled_kg: float
    total_waste_disposed_kg: float

    co2_saved_kg: float
    water_saved_liters: float
    energy_saved_kwh: float
    landfill_waste_reduced_kg: float

    calculation_method: str | None = None
    status: EnvironmentalImpactStatus

    calculated_by: int | None = None
    verified_by: int | None = None
    verified_at: datetime | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EnvironmentalImpactListResponse(BaseModel):
    total: int
    items: list[EnvironmentalImpactResponse] = Field(default_factory=list)


class EnvironmentalImpactSummary(BaseModel):
    total_reports: int = 0
    total_waste_collected_kg: float = 0
    total_waste_recycled_kg: float = 0
    total_waste_disposed_kg: float = 0
    total_co2_saved_kg: float = 0
    total_water_saved_liters: float = 0
    total_energy_saved_kwh: float = 0
    total_landfill_waste_reduced_kg: float = 0