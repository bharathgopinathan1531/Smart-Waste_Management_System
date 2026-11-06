from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.customer import Customer


def get_customer_by_id(db: Session, customer_id: int):
    return db.scalar(
        select(Customer).where(Customer.id == customer_id)
    )


def get_customer_by_email(db: Session, email: str):
    return db.scalar(
        select(Customer).where(
            func.lower(Customer.email) == email.strip().lower()
        )
    )


def get_customer_by_phone(db: Session, phone: str):
    return db.scalar(
        select(Customer).where(Customer.phone == phone.strip())
    )


def get_all_customers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    customer_type: str | None = None,
    customer_status: str | None = None,
    search: str | None = None,
):
    query = select(Customer)

    if customer_type:
        query = query.where(Customer.customer_type == customer_type)

    if customer_status:
        query = query.where(Customer.status == customer_status)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.where(
            or_(
                Customer.full_name.ilike(search_term),
                Customer.email.ilike(search_term),
                Customer.phone.ilike(search_term),
                Customer.city.ilike(search_term),
            )
        )

    query = query.order_by(Customer.id.desc())
    query = query.offset(skip).limit(limit)

    return list(db.scalars(query).all())


def count_customers(
    db: Session,
    customer_type: str | None = None,
    customer_status: str | None = None,
    search: str | None = None,
):
    query = select(func.count(Customer.id))

    if customer_type:
        query = query.where(Customer.customer_type == customer_type)

    if customer_status:
        query = query.where(Customer.status == customer_status)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.where(
            or_(
                Customer.full_name.ilike(search_term),
                Customer.email.ilike(search_term),
                Customer.phone.ilike(search_term),
                Customer.city.ilike(search_term),
            )
        )

    return db.scalar(query) or 0


def create_customer(db: Session, customer_data: dict):
    try:
        customer = Customer(**customer_data)

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    except Exception:
        db.rollback()
        raise


def update_customer(
    db: Session,
    customer: Customer,
    update_data: dict,
):
    try:
        for key, value in update_data.items():
            setattr(customer, key, value)

        db.commit()
        db.refresh(customer)

        return customer

    except Exception:
        db.rollback()
        raise


def delete_customer(db: Session, customer: Customer):
    try:
        db.delete(customer)
        db.commit()

    except Exception:
        db.rollback()
        raise