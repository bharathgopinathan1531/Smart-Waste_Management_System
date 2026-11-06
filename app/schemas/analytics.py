from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class PerformanceSummary(BaseModel):
    total_collections: int = 0
    completed_collections: int = 0
    pending_collections: int = 0
    missed_collections: int = 0
    total_quantity_collected: float = 0
    average_quantity_per_collection: float = 0
    completion_rate: float = 0


class PerformanceByPeriod(BaseModel):
    period: str
    total_collections: int = 0
    completed_collections: int = 0
    total_quantity_collected: float = 0


class DriverPerformance(BaseModel):
    driver_id: int
    driver_name: str
    total_assignments: int = 0
    completed_assignments: int = 0
    completion_rate: float = 0
    total_quantity_collected: float = 0


class VehiclePerformance(BaseModel):
    vehicle_id: int
    registration_number: str
    total_assignments: int = 0
    completed_assignments: int = 0
    total_quantity_collected: float = 0


class CollectionPerformanceResponse(BaseModel):
    start_date: date
    end_date: date
    summary: PerformanceSummary
    daily_performance: list[PerformanceByPeriod] = Field(default_factory=list)
    driver_performance: list[DriverPerformance] = Field(default_factory=list)
    vehicle_performance: list[VehiclePerformance] = Field(default_factory=list)


class PerformanceFilter(BaseModel):
    start_date: date
    end_date: date

    model_config = ConfigDict(from_attributes=True)