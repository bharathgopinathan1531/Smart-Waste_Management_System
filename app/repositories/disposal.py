from sqlalchemy.orm import Session

from app.models.disposal import WasteDisposal


def get_disposal_by_id(db: Session, disposal_id: int):
    return (
        db.query(WasteDisposal)
        .filter(WasteDisposal.id == disposal_id)
        .first()
    )


def get_disposal_by_number(db: Session, disposal_number: str):
    return (
        db.query(WasteDisposal)
        .filter(WasteDisposal.disposal_number == disposal_number)
        .first()
    )


def get_all_disposals(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    waste_category_id: int | None = None,
    disposal_method: str | None = None,
):
    query = db.query(WasteDisposal)

    if status:
        query = query.filter(WasteDisposal.status == status)

    if waste_category_id:
        query = query.filter(
            WasteDisposal.waste_category_id == waste_category_id
        )

    if disposal_method:
        query = query.filter(
            WasteDisposal.disposal_method == disposal_method
        )

    return (
        query.order_by(WasteDisposal.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_disposals(
    db: Session,
    status: str | None = None,
    waste_category_id: int | None = None,
    disposal_method: str | None = None,
):
    query = db.query(WasteDisposal)

    if status:
        query = query.filter(WasteDisposal.status == status)

    if waste_category_id:
        query = query.filter(
            WasteDisposal.waste_category_id == waste_category_id
        )

    if disposal_method:
        query = query.filter(
            WasteDisposal.disposal_method == disposal_method
        )

    return query.count()


def create_disposal(db: Session, disposal_data: dict):
    disposal = WasteDisposal(**disposal_data)

    db.add(disposal)
    db.flush()

    return disposal


def update_disposal(
    db: Session,
    disposal: WasteDisposal,
    update_data: dict,
):
    for key, value in update_data.items():
        if hasattr(disposal, key):
            setattr(disposal, key, value)

    db.flush()

    return disposal


def delete_disposal(db: Session, disposal: WasteDisposal):
    db.delete(disposal)
    db.flush()

    return True