from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.utils.enums import WorkforceRole, WorkforceStatus


class WorkforceCreate(BaseModel):
    employee_code: str = Field(min_length=2, max_length=50)
    full_name: str = Field(min_length=2, max_length=150)
    phone: str = Field(min_length=7, max_length=20)
    email: EmailStr | None = None

    role: WorkforceRole

    license_number: str | None = Field(default=None, max_length=100)
    license_expiry: datetime | None = None

    address: str | None = None
    emergency_contact: str | None = Field(default=None, max_length=20)
    notes: str | None = None

    user_id: int | None = Field(default=None, gt=0)


class WorkforceUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    phone: str | None = Field(default=None, min_length=7, max_length=20)
    email: EmailStr | None = None

    role: WorkforceRole | None = None

    license_number: str | None = Field(default=None, max_length=100)
    license_expiry: datetime | None = None

    address: str | None = None
    emergency_contact: str | None = Field(default=None, max_length=20)
    notes: str | None = None

    user_id: int | None = Field(default=None, gt=0)


class WorkforceStatusUpdate(BaseModel):
    status: WorkforceStatus


class WorkforceResponse(BaseModel):
    id: int
    employee_code: str
    full_name: str
    phone: str
    email: EmailStr | None
    role: WorkforceRole
    status: WorkforceStatus
    license_number: str | None
    license_expiry: datetime | None
    address: str | None
    emergency_contact: str | None
    notes: str | None
    user_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkforceListResponse(BaseModel):
    total: int
    employees: list[WorkforceResponse]