from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User

from app.schemas.collections import (
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
    CollectionListResponse,
)

from app.services.collections import (
    create_new_collection,
    list_collections,
    get_collection_details,
    update_existing_collection,
)


router = APIRouter(
    prefix="/collections",
    tags=["Collection Tracking"],
)


@router.post(
    "/",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_collection_endpoint(
    payload: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return create_new_collection(
        db=db,
        payload=payload,
        recorded_by=current_user.id,
    )


@router.get(
    "/",
    response_model=CollectionListResponse,
)
def get_collections(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_collections(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def get_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return get_collection_details(
        db=db,
        collection_id=collection_id,
    )


@router.patch(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def update_collection_endpoint(
    collection_id: int,
    payload: CollectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_existing_collection(
        db=db,
        collection_id=collection_id,
        payload=payload,
    )