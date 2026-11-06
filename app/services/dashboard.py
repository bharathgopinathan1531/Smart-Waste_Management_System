from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.pickup_request import PickupRequest
from app.models.collection import CollectionRecord
from app.models.vehicle import Vehicle
from app.models.recycling_center import RecyclingCenter
from app.models.complaint import CustomerComplaint
from app.models.waste_transfer import WasteTransfer
from app.models.processing_batch import ProcessingBatch
from app.models.disposal import WasteDisposal


def get_admin_dashboard(db: Session):
    total_customers = db.query(Customer).count()

    total_pickup_requests = db.query(PickupRequest).count()
    pending_pickup_requests = db.query(PickupRequest).filter(
        PickupRequest.status == "pending"
    ).count()
    completed_pickup_requests = db.query(PickupRequest).filter(
        PickupRequest.status == "completed"
    ).count()

    total_collections = db.query(CollectionRecord).count()
    total_waste_collected = (
        db.query(CollectionRecord.collected_quantity)
        .all()
    )
    total_waste_collected_kg = sum(
        float(row[0] or 0)
        for row in total_waste_collected
    )

    total_vehicles = db.query(Vehicle).count()
    available_vehicles = db.query(Vehicle).filter(
        Vehicle.status == "available"
    ).count()
    vehicles_on_route = db.query(Vehicle).filter(
        Vehicle.status == "on_route"
    ).count()

    total_recycling_centers = db.query(RecyclingCenter).count()
    active_recycling_centers = db.query(RecyclingCenter).filter(
        RecyclingCenter.status == "active"
    ).count()

    total_complaints = db.query(CustomerComplaint).count()
    open_complaints = db.query(CustomerComplaint).filter(
        CustomerComplaint.status.in_(["open", "assigned", "in_progress"])
    ).count()

    transferred_quantities = db.query(
        WasteTransfer.transferred_quantity
    ).filter(
        WasteTransfer.status.in_(["in_transit", "received"])
    ).all()

    total_waste_transferred_kg = sum(
        float(row[0] or 0)
        for row in transferred_quantities
    )

    recycled_quantities = db.query(
        ProcessingBatch.recovered_quantity
    ).filter(
        ProcessingBatch.status == "completed"
    ).all()

    total_waste_recycled_kg = sum(
        float(row[0] or 0)
        for row in recycled_quantities
    )

    disposed_quantities = db.query(
        WasteDisposal.quantity
    ).filter(
        WasteDisposal.status == "completed"
    ).all()

    total_waste_disposed_kg = sum(
        float(row[0] or 0)
        for row in disposed_quantities
    )

    return {
        "summary": {
            "total_customers": total_customers,
            "total_pickup_requests": total_pickup_requests,
            "pending_pickup_requests": pending_pickup_requests,
            "completed_pickup_requests": completed_pickup_requests,
            "total_collections": total_collections,
            "total_waste_collected_kg": total_waste_collected_kg,
            "total_vehicles": total_vehicles,
            "available_vehicles": available_vehicles,
            "vehicles_on_route": vehicles_on_route,
            "total_recycling_centers": total_recycling_centers,
            "active_recycling_centers": active_recycling_centers,
            "total_complaints": total_complaints,
            "open_complaints": open_complaints,
            "total_waste_transferred_kg": total_waste_transferred_kg,
            "total_waste_recycled_kg": total_waste_recycled_kg,
            "total_waste_disposed_kg": total_waste_disposed_kg,
            "generated_at": datetime.now(timezone.utc),
        },
        "recent_activities": [],
    }