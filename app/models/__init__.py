from app.models.user import User
from app.models.location import Location
from app.models.waste_category import WasteCategory
from app.models.customer import Customer
from app.models.pickup_request import PickupRequest
from app.models.vehicle import Vehicle
from app.models.workforce import Workforce
from app.models.assignment import CollectionAssignment
from app.models.collection import CollectionRecord
from app.models.recycling_center import RecyclingCenter
from app.models.waste_transfer import WasteTransfer
from app.models.segregation import WasteSegregation
from app.models.processing_batch import ProcessingBatch
from app.models.disposal import WasteDisposal
from app.models.maintenance import VehicleMaintenance
from app.models.complaint import CustomerComplaint
from app.models.environmental_impact import EnvironmentalImpact
from app.models.notification import Notification
from app.models.audit_log import AuditLog
__all__ = [
    "User",
    "Location",
    "WasteCategory",
    "Customer",
    "PickupRequest",
    "Vehicle",
    "Workforce",
    "CollectionRecord"
    "WasteSegregation",
    "WasteDisposal",
    "VehicleMaintenance",
    "CustomerComplaint",
    "EnvironmentalImpact",
]