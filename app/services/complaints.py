
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.complaint import CustomerComplaint
from app.models.customer import Customer
from app.models.user import User
from app.utils.enums import ComplaintStatus


def create_new_complaint(db: Session, complaint_data: dict):
    customer = (
        db.query(Customer)
        .filter(Customer.id == complaint_data["customer_id"])
        .first()
    )

    if not customer:
        raise ValueError("Customer not found")

    if str(customer.status).lower() not in (
        "active",
        "customerstatus.active",
    ):
        raise ValueError("Customer is not active")

    complaint = CustomerComplaint(
        complaint_number=(
            f"CMP-{datetime.now(timezone.utc).strftime('%Y%m%d')}-"
            f"{uuid4().hex[:8].upper()}"
        ),
        customer_id=complaint_data["customer_id"],
        category=complaint_data["category"],
        priority=complaint_data.get("priority", "normal"),
        subject=complaint_data["subject"],
        description=complaint_data["description"],
        status=ComplaintStatus.OPEN,
    )

    try:
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint
    except Exception:
        db.rollback()
        raise


def list_complaints(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    customer_id: int | None = None,
    status: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    assigned_to: int | None = None,
):
    query = db.query(CustomerComplaint)

    if customer_id is not None:
        query = query.filter(
            CustomerComplaint.customer_id == customer_id
        )

    if status is not None:
        query = query.filter(
            CustomerComplaint.status == status
        )

    if priority is not None:
        query = query.filter(
            CustomerComplaint.priority == priority
        )

    if category is not None:
        query = query.filter(
            CustomerComplaint.category == category
        )

    if assigned_to is not None:
        query = query.filter(
            CustomerComplaint.assigned_to == assigned_to
        )

    total = query.count()

    complaints = (
        query.order_by(CustomerComplaint.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "complaints": complaints,
    }


def get_complaint_details(
    db: Session,
    complaint_id: int,
):
    complaint = (
        db.query(CustomerComplaint)
        .filter(CustomerComplaint.id == complaint_id)
        .first()
    )

    if not complaint:
        raise ValueError("Complaint not found")

    return complaint


def update_existing_complaint(
    db: Session,
    complaint_id: int,
    update_data: dict,
):
    complaint = get_complaint_details(db, complaint_id)

    if complaint.status not in (
        ComplaintStatus.OPEN,
        ComplaintStatus.ASSIGNED,
    ):
        raise ValueError(
            "Only open or assigned complaints can be updated"
        )

    for field, value in update_data.items():
        setattr(complaint, field, value)

    try:
        db.commit()
        db.refresh(complaint)
        return complaint
    except Exception:
        db.rollback()
        raise


def assign_complaint(
    db: Session,
    complaint_id: int,
    assigned_to: int,
):
    complaint = get_complaint_details(db, complaint_id)

    if complaint.status not in (
        ComplaintStatus.OPEN,
        ComplaintStatus.ASSIGNED,
    ):
        raise ValueError(
            "Only open or assigned complaints can be assigned"
        )

    user = (
        db.query(User)
        .filter(User.id == assigned_to)
        .first()
    )

    if not user:
        raise ValueError("Assigned user not found")

    if not user.is_active:
        raise ValueError("Assigned user is not active")

    try:
        complaint.assigned_to = user.id
        complaint.status = ComplaintStatus.ASSIGNED

        db.commit()
        db.refresh(complaint)
        return complaint
    except Exception:
        db.rollback()
        raise


def update_complaint_status(
    db: Session,
    complaint_id: int,
    new_status: ComplaintStatus,
    resolution_notes: str | None = None,
):
    complaint = get_complaint_details(db, complaint_id)

    allowed_transitions = {
        ComplaintStatus.OPEN: [
            ComplaintStatus.ASSIGNED,
            ComplaintStatus.REJECTED,
        ],
        ComplaintStatus.ASSIGNED: [
            ComplaintStatus.IN_PROGRESS,
            ComplaintStatus.REJECTED,
        ],
        ComplaintStatus.IN_PROGRESS: [
            ComplaintStatus.RESOLVED,
            ComplaintStatus.REJECTED,
        ],
        ComplaintStatus.RESOLVED: [
            ComplaintStatus.CLOSED,
        ],
        ComplaintStatus.CLOSED: [],
        ComplaintStatus.REJECTED: [],
    }

    if new_status not in allowed_transitions[complaint.status]:
        raise ValueError(
            f"Cannot change complaint status from "
            f"{complaint.status} to {new_status}"
        )

    if new_status == ComplaintStatus.RESOLVED:
        if not resolution_notes or not resolution_notes.strip():
            raise ValueError("Resolution notes are required")

        complaint.resolution_notes = resolution_notes.strip()
        complaint.resolved_at = datetime.now(timezone.utc)

    try:
        complaint.status = new_status
        db.commit()
        db.refresh(complaint)
        return complaint
    except Exception:
        db.rollback()
        raise


def remove_complaint(
    db: Session,
    complaint_id: int,
):
    complaint = get_complaint_details(db, complaint_id)

    if complaint.status not in (
        ComplaintStatus.OPEN,
        ComplaintStatus.REJECTED,
    ):
        raise ValueError(
            "Only open or rejected complaints can be deleted"
        )

    try:
        db.delete(complaint)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
