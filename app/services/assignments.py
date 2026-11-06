from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.pickup_request import PickupRequest
from app.models.vehicle import Vehicle
from app.models.workforce import Workforce
from app.models.user import User

from app.repositories.assignment import (
    get_assignment_by_id,
    get_assignment_by_request,
    get_active_assignment_by_vehicle,
    get_active_assignment_by_driver,
    get_all_assignments,
    count_assignments,
    create_assignment,
    update_assignment,
)

from app.schemas.assignments import AssignmentCreate, AssignmentUpdate
from app.utils.enums import (
    AssignmentStatus,
    PickupRequestStatus,
    VehicleStatus,
    WorkforceRole,
    WorkforceStatus,
)


def create_new_assignment(
    db: Session,
    payload: AssignmentCreate,
    supervisor_id: int | None = None,
):
    try:
        pickup_request = db.query(PickupRequest).filter(
            PickupRequest.id == payload.pickup_request_id
        ).with_for_update().first()

        if not pickup_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pickup request not found",
            )

        if pickup_request.status != PickupRequestStatus.APPROVED.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only approved pickup requests can be assigned",
            )

        if get_assignment_by_request(db, payload.pickup_request_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pickup request already has an assignment",
            )

        vehicle = db.query(Vehicle).filter(
            Vehicle.id == payload.vehicle_id
        ).with_for_update().first()

        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found",
            )

        if vehicle.status != VehicleStatus.AVAILABLE.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle is not available",
            )

        if vehicle.capacity_kg < pickup_request.estimated_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Vehicle capacity ({vehicle.capacity_kg} kg) is lower "
                    f"than requested quantity "
                    f"({pickup_request.estimated_quantity} kg)"
                ),
            )

        if get_active_assignment_by_vehicle(db, vehicle.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vehicle already has an active assignment",
            )

        driver = db.query(Workforce).filter(
            Workforce.id == payload.driver_id
        ).with_for_update().first()

        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found",
            )

        if driver.role != WorkforceRole.DRIVER.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected employee is not registered as a driver",
            )

        if driver.status != WorkforceStatus.AVAILABLE.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driver is not available",
            )

        if get_active_assignment_by_driver(db, driver.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Driver already has an active assignment",
            )

        if supervisor_id is not None:
            supervisor = db.query(User).filter(
                User.id == supervisor_id
            ).first()

            if not supervisor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Supervisor account not found",
                )

        assignment_data = {
            "assignment_number": f"ASN-{datetime.now(timezone.utc):%Y%m%d}-{uuid4().hex[:8].upper()}",
            "pickup_request_id": pickup_request.id,
            "vehicle_id": vehicle.id,
            "driver_id": driver.id,
            "supervisor_id": supervisor_id,
            "scheduled_at": payload.scheduled_at,
            "status": AssignmentStatus.ASSIGNED.value,
            "notes": payload.notes,
        }

        assignment = create_assignment(db, assignment_data)

        pickup_request.status = PickupRequestStatus.ASSIGNED.value
        vehicle.status = VehicleStatus.ON_ROUTE.value
        driver.status = WorkforceStatus.ASSIGNED.value

        db.commit()
        db.refresh(assignment)

        return assignment

    except Exception:
        db.rollback()
        raise


def list_assignments(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    assignment_status: AssignmentStatus | None = None,
    vehicle_id: int | None = None,
    driver_id: int | None = None,
):
    status_value = (
        assignment_status.value if assignment_status else None
    )

    assignments = get_all_assignments(
        db=db,
        skip=skip,
        limit=limit,
        assignment_status=status_value,
        vehicle_id=vehicle_id,
        driver_id=driver_id,
    )

    total = count_assignments(
        db=db,
        assignment_status=status_value,
        vehicle_id=vehicle_id,
        driver_id=driver_id,
    )

    return {
        "total": total,
        "assignments": assignments,
    }


def get_assignment_details(db: Session, assignment_id: int):
    assignment = get_assignment_by_id(db, assignment_id)

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )

    return assignment


def update_existing_assignment(
    db: Session,
    assignment_id: int,
    payload: AssignmentUpdate,
):
    assignment = get_assignment_details(db, assignment_id)

    if assignment.status != AssignmentStatus.ASSIGNED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only assigned collections can be edited",
        )

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update fields provided",
        )

    try:
        updated = update_assignment(db, assignment, update_data)
        db.commit()
        db.refresh(updated)
        return updated
    except Exception:
        db.rollback()
        raise


def update_assignment_status(
    db: Session,
    assignment_id: int,
    new_status: AssignmentStatus,
    notes: str | None = None,
):
    assignment = get_assignment_details(db, assignment_id)

    allowed_transitions = {
        AssignmentStatus.ASSIGNED.value: {
            AssignmentStatus.IN_PROGRESS.value,
            AssignmentStatus.CANCELLED.value,
        },
        AssignmentStatus.IN_PROGRESS.value: {
            AssignmentStatus.COMPLETED.value,
            AssignmentStatus.CANCELLED.value,
        },
        AssignmentStatus.COMPLETED.value: set(),
        AssignmentStatus.CANCELLED.value: set(),
    }

    if new_status.value not in allowed_transitions.get(
        assignment.status, set()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot change assignment from {assignment.status} to {new_status.value}",
        )

    try:
        now = datetime.now(timezone.utc)

        assignment.status = new_status.value

        if notes is not None:
            assignment.notes = notes

        pickup_request = db.query(PickupRequest).filter(
            PickupRequest.id == assignment.pickup_request_id
        ).with_for_update().first()

        vehicle = db.query(Vehicle).filter(
            Vehicle.id == assignment.vehicle_id
        ).with_for_update().first()

        driver = db.query(Workforce).filter(
            Workforce.id == assignment.driver_id
        ).with_for_update().first()

        if not pickup_request or not vehicle or not driver:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Related pickup request, vehicle or driver is missing",
            )

        if new_status == AssignmentStatus.IN_PROGRESS:
            assignment.started_at = now
            pickup_request.status = PickupRequestStatus.IN_PROGRESS.value
            driver.status = WorkforceStatus.ON_DUTY.value

        elif new_status == AssignmentStatus.COMPLETED:
            assignment.completed_at = now
            pickup_request.status = PickupRequestStatus.COMPLETED.value
            vehicle.status = VehicleStatus.AVAILABLE.value
            driver.status = WorkforceStatus.AVAILABLE.value

        elif new_status == AssignmentStatus.CANCELLED:
            pickup_request.status = PickupRequestStatus.CANCELLED.value
            vehicle.status = VehicleStatus.AVAILABLE.value
            driver.status = WorkforceStatus.AVAILABLE.value

        db.commit()
        db.refresh(assignment)

        return assignment

    except Exception:
        db.rollback()
        raise