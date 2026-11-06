from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DashboardSummary(BaseModel):
    total_customers: int = 0
    total_pickup_requests: int = 0
    pending_pickup_requests: int = 0
    completed_pickup_requests: int = 0
    total_collections: int = 0
    total_waste_collected_kg: float = 0
    total_vehicles: int = 0
    available_vehicles: int = 0
    vehicles_on_route: int = 0
    total_recycling_centers: int = 0
    active_recycling_centers: int = 0
    total_complaints: int = 0
    open_complaints: int = 0
    total_waste_transferred_kg: float = 0
    total_waste_recycled_kg: float = 0
    total_waste_disposed_kg: float = 0
    generated_at: datetime


class DashboardRecentActivity(BaseModel):
    activity_type: str
    reference_number: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    recent_activities: list[DashboardRecentActivity] = []