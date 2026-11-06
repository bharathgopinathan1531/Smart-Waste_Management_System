from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.customer import (
    get_customer_by_id,
    get_customer_by_email,
    get_customer_by_phone,
    get_all_customers,
    count_customers,
    create_customer,
    update_customer,
    delete_customer,
)
from app.repositories.location import get_location_by_id


def create_new_customer(db: Session, payload):
    data = payload.model_dump()

    data["full_name"] = data["full_name"].strip()
    data["email"] = str(data["email"]).strip().lower()
    data["phone"] = data["phone"].strip()

    if get_customer_by_email(db, data["email"]):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer email already exists",
        )

    if get_customer_by_phone(db, data["phone"]):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer phone number already exists",
        )

    if data.get("location_id") is not None:
        location = get_location_by_id(db, data["location_id"])

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection location not found",
            )

        if location.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot assign customer to an inactive location",
            )

    if data.get("customer_type"):
        data["customer_type"] = data["customer_type"].value

    data["status"] = "active"

    return create_customer(db, data)


def list_customers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    customer_type=None,
    customer_status=None,
    search: str | None = None,
):
    type_value = customer_type.value if customer_type else None
    status_value = customer_status.value if customer_status else None

    customers = get_all_customers(
        db=db,
        skip=skip,
        limit=limit,
        customer_type=type_value,
        customer_status=status_value,
        search=search,
    )

    total = count_customers(
        db=db,
        customer_type=type_value,
        customer_status=status_value,
        search=search,
    )

    return {
        "total": total,
        "customers": customers,
    }


def get_customer_details(db: Session, customer_id: int):
    customer = get_customer_by_id(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


def update_existing_customer(
    db: Session,
    customer_id: int,
    payload,
):
    customer = get_customer_details(db, customer_id)

    data = payload.model_dump(exclude_unset=True)

    if "full_name" in data and data["full_name"] is not None:
        data["full_name"] = data["full_name"].strip()

    if "email" in data and data["email"] is not None:
        data["email"] = str(data["email"]).strip().lower()

        existing = get_customer_by_email(db, data["email"])

        if existing and existing.id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Customer email already exists",
            )

    if "phone" in data and data["phone"] is not None:
        data["phone"] = data["phone"].strip()

        existing = get_customer_by_phone(db, data["phone"])

        if existing and existing.id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Customer phone number already exists",
            )

    if "location_id" in data and data["location_id"] is not None:
        location = get_location_by_id(db, data["location_id"])

        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection location not found",
            )

        if location.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot assign customer to an inactive location",
            )

    if "customer_type" in data and data["customer_type"] is not None:
        data["customer_type"] = data["customer_type"].value

    if "status" in data and data["status"] is not None:
        data["status"] = data["status"].value

    return update_customer(db, customer, data)


def remove_customer(db: Session, customer_id: int):
    customer = get_customer_details(db, customer_id)

    delete_customer(db, customer)

    return {
        "message": "Customer deleted successfully",
        "customer_id": customer_id,
    }