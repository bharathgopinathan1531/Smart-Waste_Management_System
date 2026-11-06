from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.permissions import require_management

from app.schemas.audit_logs import AuditLogListResponse, AuditLogResponse

from app.services.audit_logs import (
    list_audit_logs,
    get_audit_log_details,
)


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
    dependencies=[Depends(require_management())],
)


@router.get(
    "/",
    response_model=AuditLogListResponse,
)
def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: int = Query(None, gt=0),
    action: str = Query(None),
    entity_type: str = Query(None),
    db: Session = Depends(get_db),
):
    try:
        return list_audit_logs(
            db=db,
            skip=skip,
            limit=limit,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get(
    "/{audit_log_id}",
    response_model=AuditLogResponse,
)
def get_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_audit_log_details(db, audit_log_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))