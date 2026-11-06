from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.schemas.environmental_impact import (
    EnvironmentalImpactCreate,
    EnvironmentalImpactStatusUpdate,
    EnvironmentalImpactResponse,
    EnvironmentalImpactListResponse,
)
from app.services import environmental_impact as impact_service


router = APIRouter(
    prefix="/environmental-impact",
    tags=["Environmental Impact"],
)


@router.post(
    "/calculate",
    response_model=EnvironmentalImpactResponse,
    status_code=201,
)
def calculate_impact(
    data: EnvironmentalImpactCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        return impact_service.calculate_environmental_impact(
            db,
            data.start_date,
            data.end_date,
            calculated_by=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=EnvironmentalImpactListResponse)
def list_impacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    return impact_service.list_environmental_impacts(
        db,
        skip=skip,
        limit=limit,
        status=status,
    )


@router.get("/{impact_id}", response_model=EnvironmentalImpactResponse)
def get_impact(
    impact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        return impact_service.get_environmental_impact(db, impact_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch(
    "/{impact_id}/verify",
    response_model=EnvironmentalImpactResponse,
)
def verify_impact(
    impact_id: int,
    data: EnvironmentalImpactStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        if data.status.value != "verified":
            raise ValueError("Only the verified status is accepted here")

        return impact_service.verify_environmental_impact(
            db,
            impact_id,
            verified_by=current_user.id,
        )
    except ValueError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(exc))


@router.delete("/{impact_id}")
def delete_impact(
    impact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        impact_service.delete_environmental_impact(db, impact_id)
        return {"message": "Environmental impact report deleted successfully"}
    except ValueError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(exc))