from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.schemas.complaints import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintAssignment,
    ComplaintStatusUpdate,
    ComplaintResponse,
    ComplaintListResponse,
)
from app.services import complaints as complaint_service


router = APIRouter(
    prefix="/complaints",
    tags=["Customer Complaints"],
)


@router.post("/", response_model=ComplaintResponse, status_code=201)
def create_complaint(
    complaint_data: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        return complaint_service.create_new_complaint(
            db,
            complaint_data.model_dump(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=ComplaintListResponse)
def get_complaints(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    customer_id: int = None,
    status: str = None,
    priority: str = None,
    category: str = None,
    assigned_to: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    return complaint_service.list_complaints(
        db,
        skip=skip,
        limit=limit,
        customer_id=customer_id,
        status=status,
        priority=priority,
        category=category,
        assigned_to=assigned_to,
    )


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        return complaint_service.get_complaint_details(db, complaint_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: int,
    update_data: ComplaintUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        return complaint_service.update_existing_complaint(
            db,
            complaint_id,
            update_data.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        status_code = 404 if str(exc) == "Complaint not found" else 400
        raise HTTPException(status_code=status_code, detail=str(exc))


@router.patch("/{complaint_id}/assign", response_model=ComplaintResponse)
def assign_complaint(
    complaint_id: int,
    assignment_data: ComplaintAssignment,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        return complaint_service.assign_complaint(
            db,
            complaint_id,
            assignment_data.assigned_to,
        )
    except ValueError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(exc))


@router.patch("/{complaint_id}/status", response_model=ComplaintResponse)
def update_complaint_status(
    complaint_id: int,
    status_data: ComplaintStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        return complaint_service.update_complaint_status(
            db,
            complaint_id,
            status_data.status,
            status_data.resolution_notes,
        )
    except ValueError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(exc))


@router.delete("/{complaint_id}")
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        complaint_service.remove_complaint(db, complaint_id)
        return {"message": "Complaint deleted successfully"}
    except ValueError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(exc))