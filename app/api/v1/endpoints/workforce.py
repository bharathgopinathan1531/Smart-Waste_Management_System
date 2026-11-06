from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.models.user import User

from app.schemas.workforce import (
    WorkforceCreate,
    WorkforceUpdate,
    WorkforceStatusUpdate,
    WorkforceResponse,
    WorkforceListResponse,
)

from app.utils.enums import WorkforceRole, WorkforceStatus

from app.services.workforce import (
    create_new_employee,
    list_employees,
    get_employee_details,
    update_existing_employee,
    update_employee_status,
    remove_employee,
)


router = APIRouter(
    prefix="/workforce",
    tags=["Driver & Worker Management"],
)


@router.post(
    "/",
    response_model=WorkforceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee_endpoint(
    payload: WorkforceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return create_new_employee(db, payload)


@router.get(
    "/",
    response_model=WorkforceListResponse,
)
def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    employee_role: WorkforceRole | None = Query(None),
    employee_status: WorkforceStatus | None = Query(None),
    search: str | None = Query(None, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_employees(
        db=db,
        skip=skip,
        limit=limit,
        employee_role=employee_role,
        employee_status=employee_status,
        search=search,
    )


@router.get(
    "/{employee_id}",
    response_model=WorkforceResponse,
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return get_employee_details(db, employee_id)


@router.patch(
    "/{employee_id}",
    response_model=WorkforceResponse,
)
def update_employee_endpoint(
    employee_id: int,
    payload: WorkforceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_existing_employee(
        db=db,
        employee_id=employee_id,
        payload=payload,
    )


@router.patch(
    "/{employee_id}/status",
    response_model=WorkforceResponse,
)
def change_employee_status(
    employee_id: int,
    payload: WorkforceStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_employee_status(
        db=db,
        employee_id=employee_id,
        new_status=payload.status,
    )


@router.delete(
    "/{employee_id}",
)
def delete_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return remove_employee(db, employee_id)