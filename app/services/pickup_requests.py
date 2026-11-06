from datetime import date
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.pickup_request import (
    get_request_by_id,
    get_all_requests,
    count_requests,
    create_request,
    update_request,
    delete_request,
)

from app.repositories.customer import get_customer_by_id
from app.repositories.location import get_location_by_id
from app.repositories.waste_category import get_category_by_id


ALLOWED_STATUS_TRANSITIONS = {
    "pending": {"approved", "rejected", "cancelled"},
    "approved": {"assigned", "cancelled"},
    "assigned": {"in_progress", "cancelled"},
    "in_progress": {"completed"},
    "completed": set(),
    "cancelled": set(),
    "rejected": set(),
}


def create_new_request(db: Session, payload):
    data = payload.model_dump()

    customer = get_customer_by_id(db, data["customer_id"])

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    if customer.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer account is inactive",
        )

    location = get_location_by_id(db, data["location_id"])

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection location not found",
        )

    if location.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection location is inactive",
        )

    category = get_category_by_id(
        db,
        data["waste_category_id"],
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waste category not found",
        )

    if category.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Waste category is inactive",
        )

    if data["requested_date"] < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pickup date cannot be in the past",
        )

    if data["location_id"] != customer.location_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pickup location must match the customer's registered location",
        )

    data["priority"] = data["priority"].value
    data["status"] = "pending"

    data["request_number"] = (
        f"SWM-{date.today().strftime('%Y%m%d')}-"
        f"{uuid4().hex[:8].upper()}"
    )

    data["quantity_unit"] = data["quantity_unit"].strip().lower()

    if not data["quantity_unit"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity unit cannot be empty",
        )

    return create_request(db, data)


def list_pickup_requests(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    request_status=None,
    priority=None,
    customer_id: int | None = None,
    location_id: int | None = None,
    search: str | None = None,
):
    status_value = (
        request_status.value if request_status else None
    )

    priority_value = (
        priority.value if priority else None
    )

    requests = get_all_requests(
        db=db,
        skip=skip,
        limit=limit,
        request_status=status_value,
        priority=priority_value,
        customer_id=customer_id,
        location_id=location_id,
        search=search,
    )

    total = count_requests(
        db=db,
        request_status=status_value,
        priority=priority_value,
        customer_id=customer_id,
        location_id=location_id,
        search=search,
    )

    return {
        "total": total,
        "requests": requests,
    }


def get_request_details(db: Session, request_id: int):
    pickup_request = get_request_by_id(db, request_id)

    if not pickup_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pickup request not found",
        )

    return pickup_request


def update_existing_request(
    db: Session,
    request_id: int,
    payload,
):
    pickup_request = get_request_details(db, request_id)

    if pickup_request.status not in {"pending", "approved"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending or approved requests can be edited",
        )

    data = payload.model_dump(exclude_unset=True)

    if "requested_date" in data and data["requested_date"] is not None:
        if data["requested_date"] < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pickup date cannot be in the past",
            )

    if "priority" in data and data["priority"] is not None:
        data["priority"] = data["priority"].value

    if "quantity_unit" in data and data["quantity_unit"] is not None:
        data["quantity_unit"] = data["quantity_unit"].strip().lower()

        if not data["quantity_unit"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity unit cannot be empty",
            )

    return update_request(db, pickup_request, data)


def update_request_status(
    db: Session,
    request_id: int,
    new_status,
    rejection_reason: str | None = None,
):
    pickup_request = get_request_details(db, request_id)

    target_status = new_status.value

    allowed = ALLOWED_STATUS_TRANSITIONS.get(
        pickup_request.status,
        set(),
    )

    if target_status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Cannot change request status from "
                f"{pickup_request.status} to {target_status}"
            ),
        )

    if target_status == "rejected" and not rejection_reason:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejection reason is required",
        )

    data = {"status": target_status}

    if target_status == "rejected":
        data["rejection_reason"] = rejection_reason.strip()

    return update_request(db, pickup_request, data)


def cancel_pickup_request(db: Session, request_id: int):
    pickup_request = get_request_details(db, request_id)

    if pickup_request.status not in {"pending", "approved"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending or approved requests can be cancelled",
        )

    return update_request(
        db,
        pickup_request,
        {"status": "cancelled"},
    )


def remove_pickup_request(db: Session, request_id: int):
    pickup_request = get_request_details(db, request_id)

    if pickup_request.status not in {"pending", "cancelled", "rejected"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending, cancelled or rejected requests can be deleted",
        )

    delete_request(db, pickup_request)

    return {
        "message": "Pickup request deleted successfully",
        "request_id": request_id,
    }