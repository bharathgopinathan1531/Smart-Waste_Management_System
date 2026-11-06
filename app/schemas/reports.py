from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class ReportFilter(BaseModel):
    start_date: date
    end_date: date


class CollectionReportItem(BaseModel):
    collection_number: str
    collected_quantity: float
    unit: str
    collection_completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class WasteCategoryReportItem(BaseModel):
    category_name: str
    total_quantity: float
    unit: str


class VehicleReportItem(BaseModel):
    registration_number: str
    vehicle_name: str
    total_collections: int
    total_quantity_kg: float


class RecyclingReportItem(BaseModel):
    batch_number: str
    input_quantity: float
    recovered_quantity: float
    rejected_quantity: float
    recovery_rate: float
    status: str


class AdvancedReportResponse(BaseModel):
    report_type: str
    start_date: date
    end_date: date
    total_records: int
    total_quantity_kg: float
    generated_at: datetime
    data: list[dict] = []