from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.processing_batch import ProcessingBatch


def get_batch_by_id(db: Session, batch_id: int):
    return db.query(ProcessingBatch).filter(
        ProcessingBatch.id == batch_id
    ).first()


def get_batch_by_number(db: Session, batch_number: str):
    return db.query(ProcessingBatch).filter(
        ProcessingBatch.batch_number == batch_number
    ).first()


def get_all_batches(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    segregation_id: int | None = None,
):
    query = db.query(ProcessingBatch)

    if status:
        query = query.filter(ProcessingBatch.status == status)

    if segregation_id:
        query = query.filter(
            ProcessingBatch.segregation_id == segregation_id
        )

    return (
        query.order_by(ProcessingBatch.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_batches(
    db: Session,
    status: str | None = None,
    segregation_id: int | None = None,
):
    query = db.query(func.count(ProcessingBatch.id))

    if status:
        query = query.filter(ProcessingBatch.status == status)

    if segregation_id:
        query = query.filter(
            ProcessingBatch.segregation_id == segregation_id
        )

    return query.scalar() or 0


def create_batch(db: Session, batch_data: dict):
    batch = ProcessingBatch(**batch_data)
    db.add(batch)
    db.flush()
    return batch


def update_batch(
    db: Session,
    batch: ProcessingBatch,
    update_data: dict,
):
    for key, value in update_data.items():
        setattr(batch, key, value)

    db.flush()
    return batch


def delete_batch(db: Session, batch: ProcessingBatch):
    db.delete(batch)
    db.flush()