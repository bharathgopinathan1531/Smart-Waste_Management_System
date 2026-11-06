from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.scalar(
        select(User).where(User.email == email.lower())
    )


def get_user_by_phone(db: Session, phone: str):
    return db.scalar(
        select(User).where(User.phone == phone)
    )


def create_user(db: Session, user_data: dict):
    user = User(**user_data)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise

def get_user_by_id(db: Session, user_id: int):
    return db.get(User, user_id)


def get_all_users(db: Session, skip: int = 0, limit: int = 20):
    return (
        db.query(User)
        .order_by(User.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_users(db: Session):
    return db.query(User).count()


def update_user(db: Session, user: User, update_data: dict):
    try:
        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise