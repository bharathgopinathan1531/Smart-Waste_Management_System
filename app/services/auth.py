from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi import HTTPException, status
from app.core.security import verify_password, hash_password
from app.models.user import User
from app.repositories.user import get_user_by_email
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)

from app.repositories.user import (
    get_user_by_email,
    get_user_by_phone,
    create_user
)
from app.schemas.auth import UserRegister
from app.core.security import hash_password
from app.utils.enums import UserRole


def register_user(db: Session, payload: UserRegister):
    email = payload.email.lower()

    if get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    if payload.phone and get_user_by_phone(db, payload.phone):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already registered"
        )

    user_data = {
        "full_name": payload.full_name,
        "email": email,
        "phone": payload.phone,
        "hashed_password": hash_password(payload.password),
        "role": UserRole.CUSTOMER.value,
        "is_active": True,
        "is_verified": False
    }

    return create_user(db, user_data)


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email.lower())

    if not user or not verify_password(
        password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    return {
        "access_token": create_access_token(
            user.id,
            user.role
        ),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer"
    }

import jwt

from app.core.security import decode_token, create_access_token
from app.models.user import User


def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    user = db.get(User, user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive"
        )

    return {
        "access_token": create_access_token(
            user.id,
            user.role
        ),
        "token_type": "bearer"
    }

def change_password(
    db: Session,
    user: User,
    current_password: str,
    new_password: str
):
    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    if current_password == new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different"
        )

    user.hashed_password = hash_password(new_password)

    try:
        db.commit()
        db.refresh(user)
        return {"message": "Password changed successfully"}
    except Exception:
        db.rollback()
        raise