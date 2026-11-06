from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.users import UserResponse
from app.core.permissions import require_admin, require_management
from app.utils.enums import UserRole
from fastapi import Query, HTTPException, status
from sqlalchemy.orm import Session
from app.services.users import deactivate_user, reactivate_user
from app.db.session import get_db
from app.core.permissions import require_admin
from app.schemas.users import (
    UserListResponse,
    UserRoleUpdate,
    UserActiveUpdate
)
from app.services.users import (
    list_users,
    get_user_details,
    change_user_role,
    change_user_status
)
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.get("/admin-check")
def admin_check(
    current_user: User = Depends(require_admin())
):
    return {
        "message": "Admin access granted",
        "user": current_user.full_name,
        "role": current_user.role
    }


@router.get("/management-check")
def management_check(
    current_user: User = Depends(require_management())
):
    return {
        "message": "Management access granted",
        "user": current_user.full_name,
        "role": current_user.role
    }

@router.get(
    "/",
    response_model=UserListResponse
)
def admin_list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin())
):
    return list_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
def admin_get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin())
):
    return get_user_details(db, user_id)


@router.patch("/{user_id}/role", response_model=UserResponse)
def admin_change_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin())
):
    return change_user_role(
        db,
        user_id,
        payload.role,
        current_admin.id
    )


@router.patch("/{user_id}/status", response_model=UserResponse)
def admin_change_user_status(
    user_id: int,
    payload: UserActiveUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin())
):
    return change_user_status(
        db,
        user_id,
        payload.is_active,
        current_admin.id
    )
@router.patch("/{user_id}/deactivate", response_model=UserResponse)
def admin_deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin())
):
    return deactivate_user(
        db,
        user_id,
        current_admin.id
    )


@router.patch("/{user_id}/reactivate", response_model=UserResponse)
def admin_reactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin())
):
    return reactivate_user(db, user_id)