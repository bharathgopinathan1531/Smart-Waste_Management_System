from sqlalchemy.orm import Session

from app.models.environmental_impact import EnvironmentalImpact


def get_impact_by_id(db: Session, impact_id: int):
    return (
        db.query(EnvironmentalImpact)
        .filter(EnvironmentalImpact.id == impact_id)
        .first()
    )


def get_impact_by_report_number(db: Session, report_number: str):
    return (
        db.query(EnvironmentalImpact)
        .filter(EnvironmentalImpact.report_number == report_number)
        .first()
    )


def get_all_impacts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status=None,
):
    query = db.query(EnvironmentalImpact)

    if status is not None:
        query = query.filter(EnvironmentalImpact.status == status)

    return (
        query.order_by(EnvironmentalImpact.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_impacts(db: Session, status=None):
    query = db.query(EnvironmentalImpact)

    if status is not None:
        query = query.filter(EnvironmentalImpact.status == status)

    return query.count()


def create_impact(db: Session, impact_data: dict):
    impact = EnvironmentalImpact(**impact_data)
    db.add(impact)
    db.flush()
    return impact


def update_impact(
    db: Session,
    impact: EnvironmentalImpact,
    update_data: dict,
):
    for key, value in update_data.items():
        if hasattr(impact, key):
            setattr(impact, key, value)

    db.flush()
    return impact


def delete_impact(db: Session, impact: EnvironmentalImpact):
    db.delete(impact)
    db.flush()
    return True