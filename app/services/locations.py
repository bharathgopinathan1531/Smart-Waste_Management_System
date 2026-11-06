from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.location import (
    get_location_by_id,
    get_location_by_code,
    get_all_locations,
    count_locations,
    create_location,
    update_location,
    delete_location
)
from app.schemas.locations import LocationCreate, LocationUpdate


def create_new_location(db: Session, payload: LocationCreate):
    code = payload.code.strip().upper()

    if get_location_by_code(db, code):
        raise HTTPException(
            status_code=409,
            detail="Location code already exists"
        )

    validate_parent_location(
        db,
        None,
        payload.parent_id
    )

    data = payload.model_dump()
    data["code"] = code
    data["location_type"] = payload.location_type.value

    return create_location(db, data)
def list_locations(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    location_type: str | None = None
):
    locations = get_all_locations(
        db, skip, limit, location_type
    )

    return {
        "total": count_locations(db),
        "locations": locations
    }


def get_location_details(db: Session, location_id: int):
    location = get_location_by_id(db, location_id)

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )

    return location


def update_existing_location(
    db: Session,
    location_id: int,
    payload: LocationUpdate
):
    location = get_location_details(db, location_id)

    data = payload.model_dump(exclude_unset=True)

    if "status" in data and data["status"] is not None:
        data["status"] = data["status"].value

    return update_location(db, location, data)


def remove_location(db: Session, location_id: int):
    location = get_location_details(db, location_id)

    if location.children:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete a location with child locations"
        )

    delete_location(db, location)

    return {"message": "Location deleted successfully"}
def validate_parent_location(
    db: Session,
    location_id: int | None,
    parent_id: int | None
):
    if parent_id is None:
        return

    if location_id is not None and parent_id == location_id:
        raise HTTPException(
            status_code=400,
            detail="A location cannot be its own parent"
        )

    parent = get_location_by_id(db, parent_id)

    if not parent:
        raise HTTPException(
            status_code=404,
            detail="Parent location not found"
        )

    if parent.status != "active":
        raise HTTPException(
            status_code=400,
            detail="Parent location is inactive"
        )

    current = parent

    while current is not None:
        if current.id == location_id:
            raise HTTPException(
                status_code=400,
                detail="Circular location hierarchy is not allowed"
            )

        current = current.parent