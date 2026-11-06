from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard import get_admin_dashboard


router = APIRouter(
    prefix="/dashboard",
    tags=["Admin Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardResponse,
    dependencies=[Depends(require_management())],
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
):
    try:
        return get_admin_dashboard(db)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate dashboard: {str(exc)}",
        )