from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.pickup_request import PickupRequest


def get_request_by_id(db: Session, request_id: int):
    return db.scalar(
        select(PickupRequest).where(
            PickupRequest.id == request_id
        )
    )


def get_request_by_number(db: Session, request_number: str):
    return db.scalar(
        select(PickupRequest).where(
            PickupRequest.request_number == request_number
        )
    )


def get_all_requests(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    request_status: str | None = None,
    priority: str | None = None,
    customer_id: int | None = None,
    location_id: int | None = None,
    search: str | None = None,
):
    query = select(PickupRequest)

    if request_status:
        query = query.where(
            PickupRequest.status == request_status
        )

    if priority:
        query = query.where(
            PickupRequest.priority == priority
        )

    if customer_id:
        query = query.where(
            PickupRequest.customer_id == customer_id
        )

    if location_id:
        query = query.where(
            PickupRequest.location_id == location_id
        )

    if search:
        term = f"%{search.strip()}%"
        query = query.where(
            or_(
                PickupRequest.request_number.ilike(term),
                PickupRequest.pickup_address.ilike(term),
            )
        )

    query = query.order_by(PickupRequest.created_at.desc())
    query = query.offset(skip).limit(limit)

    return list(db.scalars(query).all())


def count_requests(
    db: Session,
    request_status: str | None = None,
    priority: str | None = None,
    customer_id: int | None = None,
    location_id: int | None = None,
    search: str | None = None,
):
    query = select(func.count(PickupRequest.id))

    if request_status:
        query = query.where(
            PickupRequest.status == request_status
        )

    if priority:
        query = query.where(
            PickupRequest.priority == priority
        )

    if customer_id:
        query = query.where(
            PickupRequest.customer_id == customer_id
        )

    if location_id:
        query = query.where(
            PickupRequest.location_id == location_id
        )

    if search:
        term = f"%{search.strip()}%"
        query = query.where(
            or_(
                PickupRequest.request_number.ilike(term),
                PickupRequest.pickup_address.ilike(term),
            )
        )

    return db.scalar(query) or 0


def create_request(db: Session, request_data: dict):
    try:
        pickup_request = PickupRequest(**request_data)

        db.add(pickup_request)
        db.commit()
        db.refresh(pickup_request)

        return pickup_request

    except Exception:
        db.rollback()
        raise


def update_request(
    db: Session,
    pickup_request: PickupRequest,
    update_data: dict,
):
    try:
        for key, value in update_data.items():
            setattr(pickup_request, key, value)

        db.commit()
        db.refresh(pickup_request)

        return pickup_request

    except Exception:
        db.rollback()
        raise


def delete_request(db: Session, pickup_request: PickupRequest):
    try:
        db.delete(pickup_request)
        db.commit()

    except Exception:
        db.rollback()
        raise