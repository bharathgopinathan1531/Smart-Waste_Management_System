from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import WasteType, WasteCategoryStatus


class WasteCategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    code: str = Field(min_length=2, max_length=50)
    waste_type: WasteType
    description: str | None = None
    is_recyclable: bool = False
    handling_instructions: str | None = None
    default_unit: str = Field(default="kg", min_length=1, max_length=20)


class WasteCategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    code: str | None = Field(default=None, min_length=2, max_length=50)
    waste_type: WasteType | None = None
    description: str | None = None
    is_recyclable: bool | None = None
    handling_instructions: str | None = None
    default_unit: str | None = Field(default=None, min_length=1, max_length=20)
    status: WasteCategoryStatus | None = None


class WasteCategoryResponse(BaseModel):
    id: int
    name: str
    code: str
    waste_type: WasteType
    description: str | None
    is_recyclable: bool
    handling_instructions: str | None
    default_unit: str
    status: WasteCategoryStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WasteCategoryListResponse(BaseModel):
    total: int
    categories: list[WasteCategoryResponse]