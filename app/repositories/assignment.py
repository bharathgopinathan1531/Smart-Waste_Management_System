from sqlalchemy.orm import Session

from app.models.assignment import CollectionAssignment


def get_assignment_by_id(db: Session, assignment_id: int):
    return (
        db.query(CollectionAssignment)
        .filter(CollectionAssignment.id == assignment_id)
        .first()
    )


def get_assignment_by_number(db: Session, assignment_number: str):
    return (
        db.query(CollectionAssignment)
        .filter(CollectionAssignment.assignment_number == assignment_number)
        .first()
    )


def get_assignment_by_request(db: Session, pickup_request_id: int):
    return (
        db.query(CollectionAssignment)
        .filter(
            CollectionAssignment.pickup_request_id == pickup_request_id
        )
        .first()
    )


def get_active_assignment_by_vehicle(db: Session, vehicle_id: int):
    return (
        db.query(CollectionAssignment)
        .filter(
            CollectionAssignment.vehicle_id == vehicle_id,
            CollectionAssignment.status.in_(["assigned", "in_progress"]),
        )
        .first()
    )


def get_active_assignment_by_driver(db: Session, driver_id: int):
    return (
        db.query(CollectionAssignment)
        .filter(
            CollectionAssignment.driver_id == driver_id,
            CollectionAssignment.status.in_(["assigned", "in_progress"]),
        )
        .first()
    )


def get_all_assignments(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    assignment_status: str | None = None,
    vehicle_id: int | None = None,
    driver_id: int | None = None,
):
    query = db.query(CollectionAssignment)

    if assignment_status:
        query = query.filter(
            CollectionAssignment.status == assignment_status
        )

    if vehicle_id:
        query = query.filter(
            CollectionAssignment.vehicle_id == vehicle_id
        )

    if driver_id:
        query = query.filter(
            CollectionAssignment.driver_id == driver_id
        )

    return (
        query.order_by(CollectionAssignment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_assignments(
    db: Session,
    assignment_status: str | None = None,
    vehicle_id: int | None = None,
    driver_id: int | None = None,
):
    query = db.query(CollectionAssignment)

    if assignment_status:
        query = query.filter(
            CollectionAssignment.status == assignment_status
        )

    if vehicle_id:
        query = query.filter(
            CollectionAssignment.vehicle_id == vehicle_id
        )

    if driver_id:
        query = query.filter(
            CollectionAssignment.driver_id == driver_id
        )

    return query.count()


def create_assignment(db: Session, assignment_data: dict):
    try:
        assignment = CollectionAssignment(**assignment_data)
        db.add(assignment)
        db.flush()
        db.refresh(assignment)
        return assignment
    except Exception:
        db.rollback()
        raise


def update_assignment(
    db: Session,
    assignment: CollectionAssignment,
    update_data: dict,
):
    try:
        for key, value in update_data.items():
            setattr(assignment, key, value)

        db.flush()
        db.refresh(assignment)
        return assignment
    except Exception:
        db.rollback()
        raise


def delete_assignment(db: Session, assignment: CollectionAssignment):
    try:
        db.delete(assignment)
        db.flush()
        return True
    except Exception:
        db.rollback()
        raise