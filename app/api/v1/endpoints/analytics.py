from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.schemas.analytics import CollectionPerformanceResponse
from app.services.analytics import get_collection_performance


router = APIRouter(
    prefix="/analytics",
    tags=["Collection Performance"],
)


@router.get(
    "/collection-performance",
    response_model=CollectionPerformanceResponse,
)
def collection_performance(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_management()),
):
    try:
        return get_collection_performance(
            db=db,
            start_date=start_date,
            end_date=end_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )