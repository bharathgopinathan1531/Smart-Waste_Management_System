from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.utils.enums import CustomerType, CustomerStatus


class CustomerCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)

    customer_type: CustomerType = CustomerType.RESIDENTIAL

    address: str = Field(min_length=5)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    postal_code: str = Field(min_length=3, max_length=20)

    location_id: int | None = Field(default=None, gt=0)
    notes: str | None = None


class CustomerUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    customer_type: CustomerType | None = None
    address: str | None = Field(default=None, min_length=5)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    state: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, min_length=3, max_length=20)

    location_id: int | None = Field(default=None, gt=0)
    status: CustomerStatus | None = None
    notes: str | None = None


class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    customer_type: CustomerType
    address: str
    city: str
    state: str
    postal_code: str
    location_id: int | None
    status: CustomerStatus
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerListResponse(BaseModel):
    total: int
    customers: list[CustomerResponse]