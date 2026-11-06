from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.segregation import WasteSegregation


def get_segregation_by_id(db: Session, segregation_id: int):
    return db.query(WasteSegregation).filter(
        WasteSegregation.id == segregation_id
    ).first()


def get_segregation_by_number(db: Session, segregation_number: str):
    return db.query(WasteSegregation).filter(
        WasteSegregation.segregation_number == segregation_number
    ).first()


def get_all_segregations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    transfer_id: int | None = None,
    waste_category_id: int | None = None,
):
    query = db.query(WasteSegregation)

    if status:
        query = query.filter(WasteSegregation.status == status)

    if transfer_id:
        query = query.filter(WasteSegregation.transfer_id == transfer_id)

    if waste_category_id:
        query = query.filter(
            WasteSegregation.waste_category_id == waste_category_id
        )

    return (
        query.order_by(WasteSegregation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_segregations(
    db: Session,
    status: str | None = None,
    transfer_id: int | None = None,
    waste_category_id: int | None = None,
):
    query = db.query(func.count(WasteSegregation.id))

    if status:
        query = query.filter(WasteSegregation.status == status)

    if transfer_id:
        query = query.filter(WasteSegregation.transfer_id == transfer_id)

    if waste_category_id:
        query = query.filter(
            WasteSegregation.waste_category_id == waste_category_id
        )

    return query.scalar() or 0


def create_segregation(db: Session, segregation_data: dict):
    segregation = WasteSegregation(**segregation_data)
    db.add(segregation)
    db.flush()
    return segregation


def update_segregation(
    db: Session,
    segregation: WasteSegregation,
    update_data: dict,
):
    for key, value in update_data.items():
        setattr(segregation, key, value)

    db.flush()
    return segregation


def delete_segregation(db: Session, segregation: WasteSegregation):
    db.delete(segregation)
    db.flush()