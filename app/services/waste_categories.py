from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.waste_category import (
    get_category_by_id,
    get_category_by_code,
    get_category_by_name,
    get_all_categories,
    count_categories,
    create_category,
    update_category,
    delete_category,
)


def create_new_category(db: Session, payload):
    category_data = payload.model_dump()

    category_data["code"] = category_data["code"].strip().upper()
    category_data["name"] = category_data["name"].strip()

    if get_category_by_code(db, category_data["code"]):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Waste category code already exists",
        )

    if get_category_by_name(db, category_data["name"]):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Waste category name already exists",
        )

    category_data["waste_type"] = category_data["waste_type"].value

    category = create_category(db, category_data)

    return category


def list_categories(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    waste_type=None,
    category_status=None,
):
    waste_type_value = (
        waste_type.value if waste_type else None
    )

    status_value = (
        category_status.value if category_status else None
    )

    categories = get_all_categories(
        db=db,
        skip=skip,
        limit=limit,
        waste_type=waste_type_value,
        category_status=status_value,
    )

    total = count_categories(
        db=db,
        waste_type=waste_type_value,
        category_status=status_value,
    )

    return {
        "total": total,
        "categories": categories,
    }


def get_category_details(db: Session, category_id: int):
    category = get_category_by_id(db, category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waste category not found",
        )

    return category


def update_existing_category(
    db: Session,
    category_id: int,
    payload,
):
    category = get_category_details(db, category_id)

    update_data = payload.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] is not None:
        update_data["name"] = update_data["name"].strip()

        existing = get_category_by_name(
            db,
            update_data["name"],
        )

        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Waste category name already exists",
            )

    if "code" in update_data and update_data["code"] is not None:
        update_data["code"] = update_data["code"].strip().upper()

        existing = get_category_by_code(
            db,
            update_data["code"],
        )

        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Waste category code already exists",
            )

    if "waste_type" in update_data and update_data["waste_type"] is not None:
        update_data["waste_type"] = update_data["waste_type"].value

    if "status" in update_data and update_data["status"] is not None:
        update_data["status"] = update_data["status"].value

    return update_category(db, category, update_data)


def remove_category(db: Session, category_id: int):
    category = get_category_details(db, category_id)

    delete_category(db, category)

    return {
        "message": "Waste category deleted successfully",
        "category_id": category_id,
    }