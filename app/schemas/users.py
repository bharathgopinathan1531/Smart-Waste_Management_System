
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.utils.enums import UserRole, UserStatus


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserStatusUpdate(BaseModel):
    status: UserStatus
from pydantic import BaseModel, Field

from app.utils.enums import UserRole


class UserRoleUpdate(BaseModel):
    role: UserRole


class UserActiveUpdate(BaseModel):
    is_active: bool


class UserListResponse(BaseModel):
    total: int
    users: list[UserResponse]