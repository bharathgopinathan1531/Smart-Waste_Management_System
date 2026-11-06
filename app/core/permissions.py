from typing import Callable

from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.models.user import User
from app.utils.enums import UserRole


def require_roles(*allowed_roles: UserRole) -> Callable:
    allowed_values = {role.value for role in allowed_roles}

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role not in allowed_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker


def require_admin():
    return require_roles(UserRole.SUPER_ADMIN)


def require_management():
    return require_roles(
        UserRole.SUPER_ADMIN,
        UserRole.OPERATIONS_MANAGER
    )


def require_collection_staff():
    return require_roles(
        UserRole.SUPER_ADMIN,
        UserRole.OPERATIONS_MANAGER,
        UserRole.COLLECTION_SUPERVISOR,
        UserRole.DRIVER,
        UserRole.FIELD_WORKER
    )