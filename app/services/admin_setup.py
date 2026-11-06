from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password
from app.utils.enums import UserRole


def create_initial_admin(
    db: Session,
    full_name: str,
    email: str,
    password: str
):
    existing_admin = db.query(User).filter(
        User.role == UserRole.SUPER_ADMIN.value
    ).first()

    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Super admin already exists"
        )

    existing_user = db.query(User).filter(
        User.email == email.lower()
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    admin = User(
        full_name=full_name,
        email=email.lower(),
        hashed_password=hash_password(password),
        role=UserRole.SUPER_ADMIN.value,
        is_active=True,
        is_verified=True
    )

    try:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin
    except Exception:
        db.rollback()
        raise