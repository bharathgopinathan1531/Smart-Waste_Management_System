from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user import (
    get_user_by_id,
    get_all_users,
    count_users,
    update_user
)
from app.utils.enums import UserRole


def list_users(db: Session, skip: int = 0, limit: int = 20):
    users = get_all_users(db, skip, limit)

    return {
        "total": count_users(db),
        "users": users
    }


def get_user_details(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def change_user_role(
    db: Session,
    user_id: int,
    role: UserRole,
    current_admin_id: int
):
    user = get_user_details(db, user_id)

    if user.id == current_admin_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot change your own role"
        )

    return update_user(db, user, {"role": role.value})


def change_user_status(
    db: Session,
    user_id: int,
    is_active: bool,
    current_admin_id: int
):
    user = get_user_details(db, user_id)

    if user.id == current_admin_id and not is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate your own account"
        )

    return update_user(db, user, {"is_active": is_active})

def deactivate_user(
    db: Session,
    user_id: int,
    current_admin_id: int
):
    user = get_user_details(db, user_id)

    if user.id == current_admin_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate your own account"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is already inactive"
        )

    return update_user(
        db,
        user,
        {"is_active": False}
    )


def reactivate_user(
    db: Session,
    user_id: int
):
    user = get_user_details(db, user_id)

    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is already active"
        )

    return update_user(
        db,
        user,
        {"is_active": True}
    )