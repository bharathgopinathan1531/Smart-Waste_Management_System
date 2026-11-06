from sqlalchemy.orm import Session

from app.repositories.audit_log import (
    get_audit_log_by_id,
    get_all_audit_logs,
    count_audit_logs,
    create_audit_log,
)


def record_audit_log(
    db: Session,
    user_id: int = None,
    action: str = None,
    entity_type: str = None,
    entity_id: str = None,
    description: str = None,
    ip_address: str = None,
):
    if not action:
        raise ValueError("Audit action is required")

    if not entity_type:
        raise ValueError("Entity type is required")

    log_data = {
        "user_id": user_id,
        "action": action,
        "entity_type": entity_type,
        "entity_id": str(entity_id) if entity_id is not None else None,
        "description": description,
        "ip_address": ip_address,
    }

    try:
        audit_log = create_audit_log(db, log_data)
        db.commit()
        db.refresh(audit_log)
        return audit_log
    except Exception:
        db.rollback()
        raise


def list_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    action: str = None,
    entity_type: str = None,
):
    if skip < 0:
        raise ValueError("Skip cannot be negative")

    if limit < 1 or limit > 100:
        raise ValueError("Limit must be between 1 and 100")

    items = get_all_audit_logs(
        db=db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
    )

    total = count_audit_logs(
        db=db,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
    )

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


def get_audit_log_details(db: Session, audit_log_id: int):
    audit_log = get_audit_log_by_id(db, audit_log_id)

    if not audit_log:
        raise ValueError("Audit log not found")

    return audit_log