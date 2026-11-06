from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.collection import CollectionRecord


def get_collection_by_id(db: Session, collection_id: int):
    return (
        db.query(CollectionRecord)
        .filter(CollectionRecord.id == collection_id)
        .first()
    )


def get_collection_by_number(db: Session, collection_number: str):
    return (
        db.query(CollectionRecord)
        .filter(CollectionRecord.collection_number == collection_number)
        .first()
    )


def get_collection_by_assignment(db: Session, assignment_id: int):
    return (
        db.query(CollectionRecord)
        .filter(CollectionRecord.assignment_id == assignment_id)
        .first()
    )


def get_all_collections(
    db: Session,
    skip: int = 0,
    limit: int = 20,
):
    return (
        db.query(CollectionRecord)
        .order_by(CollectionRecord.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_collections(db: Session) -> int:
    return (
        db.query(func.count(CollectionRecord.id))
        .scalar()
        or 0
    )


def create_collection(db: Session, collection_data: dict):
    collection = CollectionRecord(**collection_data)

    db.add(collection)
    db.flush()
    db.refresh(collection)

    return collection


def update_collection(
    db: Session,
    collection: CollectionRecord,
    update_data: dict,
):
    for key, value in update_data.items():
        setattr(collection, key, value)

    db.flush()
    db.refresh(collection)

    return collection


def delete_collection(db: Session, collection: CollectionRecord):
    db.delete(collection)
    db.flush()