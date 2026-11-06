from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.recycling_center import RecyclingCenter
from app.models.user import User

from app.schemas.recycling_centers import (
    RecyclingCenterCreate,
    RecyclingCenterUpdate,
)

from app.utils.enums import (
    RecyclingCenterType,
    RecyclingCenterStatus,
    UserRole,
)

from app.repositories.recycling_center import (
    get_center_by_id,
    get_center_by_code,
    get_all_centers,
    count_centers,
    create_center,
    update_center,
    delete_center,
)


def validate_manager(db: Session, manager_id: int | None):
    if manager_id is None:
        return

    manager = db.query(User).filter(User.id == manager_id).first()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager user not found",
        )

    if manager.role != UserRole.RECYCLING_CENTER_MANAGER.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected user must have recycling center manager role",
        )


def create_new_center(
    db: Session,
    payload: RecyclingCenterCreate,
):
    center_code = payload.center_code.strip().upper()

    if get_center_by_code(db, center_code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Recycling center code already exists",
        )

    try:
        center_type = RecyclingCenterType(payload.center_type.strip().lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid recycling center type",
        )

    validate_manager(db, payload.manager_id)

    center_data = payload.model_dump(exclude={"center_code", "center_type"})

    center_data.update({
        "center_code": center_code,
        "center_name": payload.center_name.strip(),
        "center_type": center_type.value,
        "available_capacity_kg": payload.total_capacity_kg,
        "status": RecyclingCenterStatus.ACTIVE.value,
    })

    try:
        center = create_center(db, center_data)
        db.commit()
        db.refresh(center)
        return center

    except Exception:
        db.rollback()
        raise


def list_recycling_centers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    center_type: str | None = None,
    center_status: str | None = None,
    city: str | None = None,
):
    if center_type:
        try:
            center_type = RecyclingCenterType(center_type.lower()).value
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid recycling center type filter",
            )

    if center_status:
        try:
            center_status = RecyclingCenterStatus(center_status.lower()).value
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid recycling center status filter",
            )

    total = count_centers(
        db,
        center_type=center_type,
        center_status=center_status,
        city=city,
    )

    centers = get_all_centers(
        db,
        skip=skip,
        limit=limit,
        center_type=center_type,
        center_status=center_status,
        city=city,
    )

    return {
        "total": total,
        "centers": centers,
    }


def get_recycling_center_details(
    db: Session,
    center_id: int,
):
    center = get_center_by_id(db, center_id)

    if not center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recycling center not found",
        )

    return center


def update_existing_center(
    db: Session,
    center_id: int,
    payload: RecyclingCenterUpdate,
):
    center = get_recycling_center_details(db, center_id)

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        return center

    if "manager_id" in update_data:
        validate_manager(db, update_data["manager_id"])

    if "center_type" in update_data and update_data["center_type"]:
        try:
            update_data["center_type"] = RecyclingCenterType(
                update_data["center_type"].strip().lower()
            ).value
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid recycling center type",
            )

    if "total_capacity_kg" in update_data:
        used_capacity = (
            center.total_capacity_kg - center.available_capacity_kg
        )

        new_capacity = update_data["total_capacity_kg"]

        if new_capacity < used_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New capacity cannot be less than currently occupied capacity",
            )

        update_data["available_capacity_kg"] = new_capacity - used_capacity

    try:
        center = update_center(db, center, update_data)
        db.commit()
        db.refresh(center)
        return center

    except Exception:
        db.rollback()
        raise


def update_center_status(
    db: Session,
    center_id: int,
    new_status: str,
):
    center = get_recycling_center_details(db, center_id)

    try:
        status_value = RecyclingCenterStatus(new_status.lower()).value
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid recycling center status",
        )

    center.status = status_value

    try:
        db.commit()
        db.refresh(center)
        return center

    except Exception:
        db.rollback()
        raise


def remove_recycling_center(
    db: Session,
    center_id: int,
):
    center = get_recycling_center_details(db, center_id)

    try:
        delete_center(db, center)
        db.commit()

        return {
            "message": "Recycling center deleted successfully"
        }

    except Exception:
        db.rollback()
        raise