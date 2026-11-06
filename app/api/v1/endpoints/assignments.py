from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import require_management
from app.models.user import User

from app.schemas.assignments import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentStatusUpdate,
    AssignmentResponse,
    AssignmentListResponse,
)

from app.utils.enums import AssignmentStatus

from app.services.assignments import (
    create_new_assignment,
    list_assignments,
    get_assignment_details,
    update_existing_assignment,
    update_assignment_status,
)


router = APIRouter(
    prefix="/assignments",
    tags=["Collection Assignment Management"],
)


@router.post(
    "/",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_assignment_endpoint(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return create_new_assignment(
        db=db,
        payload=payload,
        supervisor_id=current_user.id,
    )


@router.get(
    "/",
    response_model=AssignmentListResponse,
)
def get_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    assignment_status: AssignmentStatus | None = Query(None),
    vehicle_id: int | None = Query(None, gt=0),
    driver_id: int | None = Query(None, gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return list_assignments(
        db=db,
        skip=skip,
        limit=limit,
        assignment_status=assignment_status,
        vehicle_id=vehicle_id,
        driver_id=driver_id,
    )


@router.get(
    "/{assignment_id}",
    response_model=AssignmentResponse,
)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return get_assignment_details(db, assignment_id)


@router.patch(
    "/{assignment_id}",
    response_model=AssignmentResponse,
)
def update_assignment_endpoint(
    assignment_id: int,
    payload: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_existing_assignment(
        db=db,
        assignment_id=assignment_id,
        payload=payload,
    )


@router.patch(
    "/{assignment_id}/status",
    response_model=AssignmentResponse,
)
def change_assignment_status(
    assignment_id: int,
    payload: AssignmentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_management()),
):
    return update_assignment_status(
        db=db,
        assignment_id=assignment_id,
        new_status=payload.status,
        notes=payload.notes,
    )