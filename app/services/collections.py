
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.assignment import CollectionAssignment
from app.models.collection import CollectionRecord
from app.models.pickup_request import PickupRequest
from app.models.vehicle import Vehicle

from app.schemas.collections import CollectionCreate, CollectionUpdate

from app.repositories.collection import (
    get_collection_by_id,
    get_collection_by_assignment,
    get_all_collections,
    count_collections,
    create_collection,
    update_collection,
)

from app.utils.enums import AssignmentStatus, PickupRequestStatus


def create_new_collection(
    db: Session,
    payload: CollectionCreate,
    recorded_by: int | None = None,
):
    try:
        assignment = (
            db.query(CollectionAssignment)
            .filter(CollectionAssignment.id == payload.assignment_id)
            .with_for_update()
            .first()
        )

        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection assignment not found",
            )

        # Check for an existing collection before checking assignment status.
        existing = get_collection_by_assignment(
            db,
            payload.assignment_id,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A collection record already exists for this assignment",
            )

        if assignment.status != AssignmentStatus.IN_PROGRESS.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only in-progress assignments can be recorded as collected",
            )

        pickup_request = (
            db.query(PickupRequest)
            .filter(PickupRequest.id == assignment.pickup_request_id)
            .first()
        )

        if not pickup_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Related pickup request not found",
            )

        vehicle = (
            db.query(Vehicle)
            .filter(Vehicle.id == assignment.vehicle_id)
            .first()
        )

        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned vehicle not found",
            )

        if payload.collected_quantity > vehicle.capacity_kg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Collected quantity exceeds vehicle capacity",
            )

        started_at = payload.collection_started_at

        if started_at and started_at > datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Collection start time cannot be in the future",
            )

        collection_number = (
            f"COL-{datetime.now(timezone.utc):%Y%m%d}-"
            f"{uuid4().hex[:8].upper()}"
        )

        collection = create_collection(
            db,
            {
                "collection_number": collection_number,
                "assignment_id": assignment.id,
                "collected_quantity": payload.collected_quantity,
                "quantity_unit": payload.quantity_unit,
                "collection_address": payload.collection_address,
                "latitude": payload.latitude,
                "longitude": payload.longitude,
                "collection_started_at": started_at,
                "collection_completed_at": datetime.now(timezone.utc),
                "proof_image_url": payload.proof_image_url,
                "notes": payload.notes,
                "recorded_by": recorded_by,
            },
        )

        assignment.status = AssignmentStatus.COMPLETED.value
        assignment.completed_at = datetime.now(timezone.utc)

        pickup_request.status = PickupRequestStatus.COMPLETED.value

        db.add(assignment)
        db.add(pickup_request)

        db.commit()
        db.refresh(collection)

        return collection

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise


def list_collections(
    db: Session,
    skip: int = 0,
    limit: int = 20,
):
    total = count_collections(db)

    collections = get_all_collections(
        db,
        skip=skip,
        limit=limit,
    )

    return {
        "total": total,
        "collections": collections,
    }


def get_collection_details(
    db: Session,
    collection_id: int,
):
    collection = get_collection_by_id(db, collection_id)

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection record not found",
        )

    return collection


def update_existing_collection(
    db: Session,
    collection_id: int,
    payload: CollectionUpdate,
):
    collection = get_collection_details(db, collection_id)

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        return collection

    try:
        if (
            "collected_quantity" in update_data
            and update_data["collected_quantity"] is not None
        ):
            assignment = collection.assignment

            vehicle = (
                db.query(Vehicle)
                .filter(Vehicle.id == assignment.vehicle_id)
                .first()
            )

            if (
                vehicle
                and update_data["collected_quantity"] > vehicle.capacity_kg
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Collected quantity exceeds vehicle capacity",
                )

        collection = update_collection(
            db,
            collection,
            update_data,
        )

        db.commit()
        db.refresh(collection)

        return collection

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise
