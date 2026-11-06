from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.services.reports import (
    get_collection_report,
    get_waste_category_report,
    get_vehicle_report,
    get_recycling_report,
)


router = APIRouter(
    prefix="/reports",
    tags=["Advanced Reports"],
    dependencies=[Depends(require_management())],
)


def validate_dates(start_date: date, end_date: date):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date",
        )


@router.get("/collections")
def collection_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    validate_dates(start_date, end_date)

    try:
        return get_collection_report(db, start_date, end_date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/waste-categories")
def waste_category_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    validate_dates(start_date, end_date)

    try:
        return get_waste_category_report(db, start_date, end_date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/vehicles")
def vehicle_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    validate_dates(start_date, end_date)

    try:
        return get_vehicle_report(db, start_date, end_date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/recycling")
def recycling_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    validate_dates(start_date, end_date)

    try:
        return get_recycling_report(db, start_date, end_date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))