from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User

from app.schemas.waste_categories import (
    WasteCategoryCreate,
    WasteCategoryUpdate,
    WasteCategoryResponse,
    WasteCategoryListResponse,
)

from app.utils.enums import WasteType, WasteCategoryStatus

from app.services.waste_categories import (
    create_new_category,
    list_categories,
    get_category_details,
    update_existing_category,
    remove_category,
)


router = APIRouter(
    prefix="/waste-categories",
    tags=["Waste Category Management"],
)


@router.post(
    "/",
    response_model=WasteCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_waste_category(
    payload: WasteCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return create_new_category(db, payload)


@router.get(
    "/",
    response_model=WasteCategoryListResponse,
)
def get_waste_categories(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    waste_type: WasteType | None = Query(default=None),
    category_status: WasteCategoryStatus | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_categories(
        db=db,
        skip=skip,
        limit=limit,
        waste_type=waste_type,
        category_status=category_status,
    )


@router.get(
    "/{category_id}",
    response_model=WasteCategoryResponse,
)
def get_waste_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return get_category_details(db, category_id)


@router.patch(
    "/{category_id}",
    response_model=WasteCategoryResponse,
)
def update_waste_category(
    category_id: int,
    payload: WasteCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_existing_category(
        db=db,
        category_id=category_id,
        payload=payload,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
)
def delete_waste_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return remove_category(db, category_id)