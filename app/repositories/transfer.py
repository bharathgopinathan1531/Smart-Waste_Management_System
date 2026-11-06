from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.waste_transfer import WasteTransfer


def get_transfer_by_id(db: Session, transfer_id: int):
    return db.query(WasteTransfer).filter(
        WasteTransfer.id == transfer_id
    ).first()


def get_transfer_by_number(db: Session, transfer_number: str):
    return db.query(WasteTransfer).filter(
        WasteTransfer.transfer_number == transfer_number
    ).first()


def get_all_transfers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    recycling_center_id: int | None = None,
    collection_id: int | None = None,
):
    query = db.query(WasteTransfer)

    if status:
        query = query.filter(WasteTransfer.status == status)

    if recycling_center_id:
        query = query.filter(
            WasteTransfer.recycling_center_id == recycling_center_id
        )

    if collection_id:
        query = query.filter(WasteTransfer.collection_id == collection_id)

    return (
        query.order_by(WasteTransfer.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_transfers(
    db: Session,
    status: str | None = None,
    recycling_center_id: int | None = None,
    collection_id: int | None = None,
):
    query = db.query(func.count(WasteTransfer.id))

    if status:
        query = query.filter(WasteTransfer.status == status)

    if recycling_center_id:
        query = query.filter(
            WasteTransfer.recycling_center_id == recycling_center_id
        )

    if collection_id:
        query = query.filter(WasteTransfer.collection_id == collection_id)

    return query.scalar() or 0


def create_transfer(db: Session, transfer_data: dict):
    transfer = WasteTransfer(**transfer_data)
    db.add(transfer)
    db.flush()
    return transfer


def update_transfer(db: Session, transfer: WasteTransfer, update_data: dict):
    for key, value in update_data.items():
        setattr(transfer, key, value)

    db.flush()
    return transfer


def delete_transfer(db: Session, transfer: WasteTransfer):
    db.delete(transfer)
    db.flush()