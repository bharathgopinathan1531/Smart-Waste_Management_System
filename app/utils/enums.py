from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    OPERATIONS_MANAGER = "operations_manager"
    COLLECTION_SUPERVISOR = "collection_supervisor"
    DRIVER = "driver"
    RECYCLING_CENTER_MANAGER = "recycling_center_manager"
    FIELD_WORKER = "field_worker"
    CUSTOMER = "customer"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class LocationType(str, Enum):
    COLLECTION_ZONE = "collection_zone"
    WARD = "ward"
    STREET = "street"
    LANDMARK = "landmark"


class LocationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class WasteType(str, Enum):
    RECYCLABLE = "recyclable"
    ORGANIC = "organic"
    HAZARDOUS = "hazardous"
    GENERAL = "general"
    E_WASTE = "e_waste"
    BIOMEDICAL = "biomedical"
    CONSTRUCTION = "construction"
    OTHER = "other"


class WasteCategoryStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    INSTITUTIONAL = "institutional"


class CustomerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class PickupRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class PickupPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class VehicleType(str, Enum):
    TRUCK = "truck"
    COMPACTOR = "compactor"
    MINI_TRUCK = "mini_truck"
    TRACTOR = "tractor"
    TIPPER = "tipper"
    OTHER = "other"


class VehicleStatus(str, Enum):
    AVAILABLE = "available"
    ON_ROUTE = "on_route"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"


class FuelType(str, Enum):
    DIESEL = "diesel"
    PETROL = "petrol"
    CNG = "cng"
    ELECTRIC = "electric"
    HYBRID = "hybrid"

class WorkforceRole(str, Enum):
    DRIVER = "driver"
    FIELD_WORKER = "field_worker"
    COLLECTION_SUPERVISOR = "collection_supervisor"


class WorkforceStatus(str, Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    ON_DUTY = "on_duty"
    ON_LEAVE = "on_leave"
    INACTIVE = "inactive"
class AssignmentStatus(str, Enum):
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class RecyclingCenterType(str, Enum):
    MATERIAL_RECOVERY = "material_recovery"
    COMPOSTING = "composting"
    E_WASTE = "e_waste"
    HAZARDOUS_WASTE = "hazardous_waste"
    GENERAL_RECYCLING = "general_recycling"
    OTHER = "other"


class RecyclingCenterStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"

class WasteTransferStatus(str, Enum):
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    RECEIVED = "received"
    CANCELLED = "cancelled"


class WasteTransferType(str, Enum):
    DIRECT = "direct"
    INTERMEDIATE = "intermediate"

class SegregationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SegregationQuality(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
class ProcessingStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProcessingMethod(str, Enum):
    SHREDDING = "shredding"
    COMPACTING = "compacting"
    MELTING = "melting"
    COMPOSTING = "composting"
    SORTING = "sorting"
    OTHER = "other"

class DisposalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DisposalMethod(str, Enum):
    LANDFILL = "landfill"
    INCINERATION = "incineration"
    SECURE_LANDFILL = "secure_landfill"
    COMPOSTING = "composting"
    OTHER = "other"

class MaintenanceType(str, Enum):
    ROUTINE_SERVICE = "routine_service"
    REPAIR = "repair"
    INSPECTION = "inspection"
    EMERGENCY_REPAIR = "emergency_repair"
    TIRE_REPLACEMENT = "tire_replacement"
    OTHER = "other"


class MaintenanceStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MaintenancePriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class ComplaintStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"


class ComplaintPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class ComplaintCategory(str, Enum):
    MISSED_PICKUP = "missed_pickup"
    DELAYED_COLLECTION = "delayed_collection"
    STAFF_BEHAVIOR = "staff_behavior"
    VEHICLE_ISSUE = "vehicle_issue"
    WASTE_HANDLING = "waste_handling"
    BILLING = "billing"
    OTHER = "other"

class PerformancePeriod(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PerformanceMetric(str, Enum):
    COLLECTION_QUANTITY = "collection_quantity"
    COMPLETED_COLLECTIONS = "completed_collections"
    MISSED_COLLECTIONS = "missed_collections"
    VEHICLE_UTILIZATION = "vehicle_utilization"
    DRIVER_PERFORMANCE = "driver_performance"

class EnvironmentalMetric(str, Enum):
    CO2_SAVED = "co2_saved"
    WATER_SAVED = "water_saved"
    ENERGY_SAVED = "energy_saved"
    LANDFILL_WASTE_REDUCED = "landfill_waste_reduced"


class EnvironmentalImpactStatus(str, Enum):
    CALCULATED = "calculated"
    VERIFIED = "verified"

class NotificationType(str, Enum):
    PICKUP_REQUEST = "pickup_request"
    COLLECTION = "collection"
    ASSIGNMENT = "assignment"
    COMPLAINT = "complaint"
    MAINTENANCE = "maintenance"
    SYSTEM = "system"
    REMINDER = "reminder"


class NotificationChannel(str, Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"


class NotificationStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"