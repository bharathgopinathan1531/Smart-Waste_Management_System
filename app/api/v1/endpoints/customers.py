from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User

from app.schemas.customers import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerListResponse,
)

from app.utils.enums import CustomerType, CustomerStatus

from app.services.customers import (
    create_new_customer,
    list_customers,
    get_customer_details,
    update_existing_customer,
    remove_customer,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customer Management"],
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_endpoint(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return create_new_customer(db, payload)


@router.get(
    "/",
    response_model=CustomerListResponse,
)
def get_customers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    customer_type: CustomerType | None = Query(default=None),
    customer_status: CustomerStatus | None = Query(default=None),
    search: str | None = Query(default=None, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_customers(
        db=db,
        skip=skip,
        limit=limit,
        customer_type=customer_type,
        customer_status=customer_status,
        search=search,
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return get_customer_details(db, customer_id)


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer_endpoint(
    customer_id: int,
    payload: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_existing_customer(
        db=db,
        customer_id=customer_id,
        payload=payload,
    )


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_200_OK,
)
def delete_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return remove_customer(db, customer_id)