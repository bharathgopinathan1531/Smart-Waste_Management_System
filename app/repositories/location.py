from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.location import Location


def get_location_by_id(db: Session, location_id: int):
    return db.get(Location, location_id)


def get_location_by_code(db: Session, code: str):
    return db.scalar(
        select(Location).where(Location.code == code.upper())
    )


def get_all_locations(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    location_type: str | None = None
):
    query = select(Location)

    if location_type:
        query = query.where(Location.location_type == location_type)

    return list(
        db.scalars(
            query.order_by(Location.id.desc())
            .offset(skip)
            .limit(limit)
        ).all()
    )


def count_locations(db: Session):
    return db.scalar(
        select(func.count()).select_from(Location)
    ) or 0


def create_location(db: Session, location_data: dict):
    location = Location(**location_data)

    try:
        db.add(location)
        db.commit()
        db.refresh(location)
        return location
    except Exception:
        db.rollback()
        raise


def update_location(db: Session, location: Location, data: dict):
    try:
        for key, value in data.items():
            setattr(location, key, value)

        db.commit()
        db.refresh(location)
        return location
    except Exception:
        db.rollback()
        raise


def delete_location(db: Session, location: Location):
    try:
        db.delete(location)
        db.commit()
    except Exception:
        db.rollback()
        raise