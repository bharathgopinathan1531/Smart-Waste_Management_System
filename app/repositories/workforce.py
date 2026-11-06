from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.workforce import Workforce


def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Workforce).filter(Workforce.id == employee_id).first()


def get_employee_by_code(db: Session, employee_code: str):
    return db.query(Workforce).filter(
        Workforce.employee_code == employee_code
    ).first()


def get_employee_by_phone(db: Session, phone: str):
    return db.query(Workforce).filter(Workforce.phone == phone).first()


def get_employee_by_email(db: Session, email: str):
    return db.query(Workforce).filter(Workforce.email == email).first()


def get_employee_by_license(db: Session, license_number: str):
    return db.query(Workforce).filter(
        Workforce.license_number == license_number
    ).first()


def get_employee_by_user_id(db: Session, user_id: int):
    return db.query(Workforce).filter(Workforce.user_id == user_id).first()


def get_all_employees(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    employee_role: str | None = None,
    employee_status: str | None = None,
    search: str | None = None,
):
    query = db.query(Workforce)

    if employee_role:
        query = query.filter(Workforce.role == employee_role)

    if employee_status:
        query = query.filter(Workforce.status == employee_status)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Workforce.employee_code.ilike(search_term),
                Workforce.full_name.ilike(search_term),
                Workforce.phone.ilike(search_term),
                Workforce.email.ilike(search_term),
            )
        )

    return (
        query.order_by(Workforce.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_employees(
    db: Session,
    employee_role: str | None = None,
    employee_status: str | None = None,
    search: str | None = None,
):
    query = db.query(Workforce)

    if employee_role:
        query = query.filter(Workforce.role == employee_role)

    if employee_status:
        query = query.filter(Workforce.status == employee_status)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Workforce.employee_code.ilike(search_term),
                Workforce.full_name.ilike(search_term),
                Workforce.phone.ilike(search_term),
                Workforce.email.ilike(search_term),
            )
        )

    return query.count()


def create_employee(db: Session, employee_data: dict):
    try:
        employee = Workforce(**employee_data)
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except Exception:
        db.rollback()
        raise


def update_employee(db: Session, employee: Workforce, update_data: dict):
    try:
        for key, value in update_data.items():
            setattr(employee, key, value)

        db.commit()
        db.refresh(employee)
        return employee
    except Exception:
        db.rollback()
        raise


def delete_employee(db: Session, employee: Workforce):
    try:
        db.delete(employee)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise