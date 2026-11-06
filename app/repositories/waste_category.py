from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.waste_category import WasteCategory


def get_category_by_id(db: Session, category_id: int):
    return db.scalar(
        select(WasteCategory).where(
            WasteCategory.id == category_id
        )
    )


def get_category_by_code(db: Session, code: str):
    return db.scalar(
        select(WasteCategory).where(
            func.upper(WasteCategory.code) == code.upper()
        )
    )


def get_category_by_name(db: Session, name: str):
    return db.scalar(
        select(WasteCategory).where(
            func.lower(WasteCategory.name) == name.lower()
        )
    )


def get_all_categories(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    waste_type: str | None = None,
    category_status: str | None = None,
):
    query = select(WasteCategory)

    if waste_type:
        query = query.where(
            WasteCategory.waste_type == waste_type
        )

    if category_status:
        query = query.where(
            WasteCategory.status == category_status
        )

    query = query.order_by(WasteCategory.id.desc())
    query = query.offset(skip).limit(limit)

    return list(db.scalars(query).all())


def count_categories(
    db: Session,
    waste_type: str | None = None,
    category_status: str | None = None,
):
    query = select(func.count(WasteCategory.id))

    if waste_type:
        query = query.where(
            WasteCategory.waste_type == waste_type
        )

    if category_status:
        query = query.where(
            WasteCategory.status == category_status
        )

    return db.scalar(query) or 0


def create_category(db: Session, category_data: dict):
    try:
        category = WasteCategory(**category_data)

        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    except Exception:
        db.rollback()
        raise


def update_category(
    db: Session,
    category: WasteCategory,
    update_data: dict,
):
    try:
        for key, value in update_data.items():
            setattr(category, key, value)

        db.commit()
        db.refresh(category)

        return category

    except Exception:
        db.rollback()
        raise


def delete_category(db: Session, category: WasteCategory):
    try:
        db.delete(category)
        db.commit()

    except Exception:
        db.rollback()
        raise