from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.recycling_center import RecyclingCenter


def get_center_by_id(db: Session, center_id: int):
    return (
        db.query(RecyclingCenter)
        .filter(RecyclingCenter.id == center_id)
        .first()
    )


def get_center_by_code(db: Session, center_code: str):
    return (
        db.query(RecyclingCenter)
        .filter(RecyclingCenter.center_code == center_code)
        .first()
    )


def get_all_centers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    center_type: str | None = None,
    center_status: str | None = None,
    city: str | None = None,
):
    query = db.query(RecyclingCenter)

    if center_type:
        query = query.filter(RecyclingCenter.center_type == center_type)

    if center_status:
        query = query.filter(RecyclingCenter.status == center_status)

    if city:
        query = query.filter(RecyclingCenter.city.ilike(f"%{city}%"))

    return (
        query.order_by(RecyclingCenter.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_centers(
    db: Session,
    center_type: str | None = None,
    center_status: str | None = None,
    city: str | None = None,
) -> int:
    query = db.query(func.count(RecyclingCenter.id))

    if center_type:
        query = query.filter(RecyclingCenter.center_type == center_type)

    if center_status:
        query = query.filter(RecyclingCenter.status == center_status)

    if city:
        query = query.filter(RecyclingCenter.city.ilike(f"%{city}%"))

    return query.scalar() or 0


def create_center(db: Session, center_data: dict):
    center = RecyclingCenter(**center_data)

    db.add(center)
    db.flush()
    db.refresh(center)

    return center


def update_center(
    db: Session,
    center: RecyclingCenter,
    update_data: dict,
):
    for key, value in update_data.items():
        setattr(center, key, value)

    db.flush()
    db.refresh(center)

    return center


def delete_center(db: Session, center: RecyclingCenter):
    db.delete(center)
    db.flush()