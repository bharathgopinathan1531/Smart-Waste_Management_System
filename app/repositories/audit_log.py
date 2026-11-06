from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def get_audit_log_by_id(db: Session, audit_log_id: int):
    return (
        db.query(AuditLog)
        .filter(AuditLog.id == audit_log_id)
        .first()
    )


def get_all_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    action: str = None,
    entity_type: str = None,
):
    query = db.query(AuditLog)

    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)

    if action:
        query = query.filter(AuditLog.action == action)

    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)

    return (
        query.order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_audit_logs(
    db: Session,
    user_id: int = None,
    action: str = None,
    entity_type: str = None,
):
    query = db.query(AuditLog)

    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)

    if action:
        query = query.filter(AuditLog.action == action)

    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)

    return query.count()


def create_audit_log(db: Session, log_data: dict):
    audit_log = AuditLog(**log_data)
    db.add(audit_log)
    db.flush()
    return audit_log