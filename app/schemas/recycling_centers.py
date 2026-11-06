from pydantic import BaseModel, ConfigDict, Field, EmailStr


class RecyclingCenterCreate(BaseModel):
    center_name: str = Field(min_length=2, max_length=150)
    center_code: str = Field(min_length=2, max_length=50)
    center_type: str

    manager_id: int | None = Field(default=None, gt=0)

    address: str = Field(min_length=5, max_length=500)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)

    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    total_capacity_kg: float = Field(gt=0)

    operating_hours: str | None = Field(default=None, max_length=200)
    contact_phone: str | None = Field(default=None, max_length=20)
    contact_email: EmailStr | None = None

    notes: str | None = None


class RecyclingCenterUpdate(BaseModel):
    center_name: str | None = Field(default=None, min_length=2, max_length=150)
    center_type: str | None = None
    manager_id: int | None = Field(default=None, gt=0)

    address: str | None = Field(default=None, min_length=5, max_length=500)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    state: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)

    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    total_capacity_kg: float | None = Field(default=None, gt=0)

    operating_hours: str | None = Field(default=None, max_length=200)
    contact_phone: str | None = Field(default=None, max_length=20)
    contact_email: EmailStr | None = None

    notes: str | None = None


class RecyclingCenterStatusUpdate(BaseModel):
    status: str


class RecyclingCenterResponse(BaseModel):
    id: int
    center_name: str
    center_code: str
    center_type: str
    manager_id: int | None
    address: str
    city: str
    state: str
    postal_code: str | None
    latitude: float | None
    longitude: float | None
    total_capacity_kg: float
    available_capacity_kg: float
    operating_hours: str | None
    contact_phone: str | None
    contact_email: str | None
    status: str
    notes: str | None
    created_at: object
    updated_at: object

    model_config = ConfigDict(from_attributes=True)


class RecyclingCenterListResponse(BaseModel):
    total: int
    centers: list[RecyclingCenterResponse]