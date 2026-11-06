from sqlalchemy.orm import Session

from app.models.complaint import CustomerComplaint


def get_complaint_by_id(db: Session, complaint_id: int):
    return (
        db.query(CustomerComplaint)
        .filter(CustomerComplaint.id == complaint_id)
        .first()
    )


def get_complaint_by_number(db: Session, complaint_number: str):
    return (
        db.query(CustomerComplaint)
        .filter(CustomerComplaint.complaint_number == complaint_number)
        .first()
    )


def get_all_complaints(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    customer_id: int = None,
    status=None,
    priority=None,
    category=None,
    assigned_to: int = None,
):
    query = db.query(CustomerComplaint)

    if customer_id is not None:
        query = query.filter(CustomerComplaint.customer_id == customer_id)

    if status is not None:
        query = query.filter(CustomerComplaint.status == status)

    if priority is not None:
        query = query.filter(CustomerComplaint.priority == priority)

    if category is not None:
        query = query.filter(CustomerComplaint.category == category)

    if assigned_to is not None:
        query = query.filter(CustomerComplaint.assigned_to == assigned_to)

    return (
        query.order_by(CustomerComplaint.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_complaints(
    db: Session,
    customer_id: int = None,
    status=None,
    priority=None,
    category=None,
    assigned_to: int = None,
):
    query = db.query(CustomerComplaint)

    if customer_id is not None:
        query = query.filter(CustomerComplaint.customer_id == customer_id)

    if status is not None:
        query = query.filter(CustomerComplaint.status == status)

    if priority is not None:
        query = query.filter(CustomerComplaint.priority == priority)

    if category is not None:
        query = query.filter(CustomerComplaint.category == category)

    if assigned_to is not None:
        query = query.filter(CustomerComplaint.assigned_to == assigned_to)

    return query.count()


def create_complaint(db: Session, complaint_data: dict):
    complaint = CustomerComplaint(**complaint_data)
    db.add(complaint)
    db.flush()
    return complaint


def update_complaint(
    db: Session,
    complaint: CustomerComplaint,
    update_data: dict,
):
    for key, value in update_data.items():
        if hasattr(complaint, key):
            setattr(complaint, key, value)

    db.flush()
    return complaint


def delete_complaint(db: Session, complaint: CustomerComplaint):
    db.delete(complaint)
    db.flush()
    return True