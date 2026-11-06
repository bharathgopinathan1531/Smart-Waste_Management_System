from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.workforce import (
    get_employee_by_id,
    get_employee_by_code,
    get_employee_by_phone,
    get_employee_by_email,
    get_employee_by_license,
    get_employee_by_user_id,
    get_all_employees,
    count_employees,
    create_employee,
    update_employee,
    delete_employee,
)
from app.schemas.workforce import WorkforceCreate, WorkforceUpdate
from app.utils.enums import WorkforceRole, WorkforceStatus, UserRole


def create_new_employee(db: Session, payload: WorkforceCreate):
    employee_code = payload.employee_code.strip().upper()
    phone = payload.phone.strip()

    if get_employee_by_code(db, employee_code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee code already exists",
        )

    if get_employee_by_phone(db, phone):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already exists",
        )

    email = str(payload.email).strip().lower() if payload.email else None

    if email and get_employee_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email address already exists",
        )

    license_number = (
        payload.license_number.strip().upper()
        if payload.license_number
        else None
    )

    if license_number and get_employee_by_license(db, license_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Driving license number already exists",
        )

    if payload.role == WorkforceRole.DRIVER and not license_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driving license number is required for drivers",
        )

    if payload.role != WorkforceRole.DRIVER and license_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driving license details are only allowed for drivers",
        )

    if payload.user_id:
        user = db.query(User).filter(User.id == payload.user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Linked user account not found",
            )

        if get_employee_by_user_id(db, payload.user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User account is already linked to an employee",
            )

        expected_role = (
            UserRole.DRIVER
            if payload.role == WorkforceRole.DRIVER
            else UserRole.FIELD_WORKER
            if payload.role == WorkforceRole.FIELD_WORKER
            else UserRole.COLLECTION_SUPERVISOR
        )

        if user.role != expected_role.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account role does not match workforce role",
            )

    employee_data = payload.model_dump()

    employee_data["employee_code"] = employee_code
    employee_data["phone"] = phone
    employee_data["email"] = email
    employee_data["license_number"] = license_number
    employee_data["role"] = payload.role.value
    employee_data["status"] = WorkforceStatus.AVAILABLE.value

    return create_employee(db, employee_data)


def list_employees(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    employee_role: WorkforceRole | None = None,
    employee_status: WorkforceStatus | None = None,
    search: str | None = None,
):
    role_value = employee_role.value if employee_role else None
    status_value = employee_status.value if employee_status else None

    employees = get_all_employees(
        db=db,
        skip=skip,
        limit=limit,
        employee_role=role_value,
        employee_status=status_value,
        search=search,
    )

    total = count_employees(
        db=db,
        employee_role=role_value,
        employee_status=status_value,
        search=search,
    )

    return {
        "total": total,
        "employees": employees,
    }


def get_employee_details(db: Session, employee_id: int):
    employee = get_employee_by_id(db, employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return employee


def update_existing_employee(
    db: Session,
    employee_id: int,
    payload: WorkforceUpdate,
):
    employee = get_employee_details(db, employee_id)

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update fields provided",
        )

    if "phone" in update_data and update_data["phone"]:
        phone = update_data["phone"].strip()
        existing = get_employee_by_phone(db, phone)

        if existing and existing.id != employee_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone number already exists",
            )

        update_data["phone"] = phone

    if "email" in update_data:
        email = (
            str(update_data["email"]).strip().lower()
            if update_data["email"]
            else None
        )

        if email:
            existing = get_employee_by_email(db, email)

            if existing and existing.id != employee_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email address already exists",
                )

        update_data["email"] = email

    if "license_number" in update_data:
        license_number = (
            update_data["license_number"].strip().upper()
            if update_data["license_number"]
            else None
        )

        if license_number:
            existing = get_employee_by_license(db, license_number)

            if existing and existing.id != employee_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Driving license number already exists",
                )

        update_data["license_number"] = license_number

    if "role" in update_data and update_data["role"]:
        update_data["role"] = update_data["role"].value

    if "user_id" in update_data and update_data["user_id"]:
        user = db.query(User).filter(
            User.id == update_data["user_id"]
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Linked user account not found",
            )

        existing = get_employee_by_user_id(db, update_data["user_id"])

        if existing and existing.id != employee_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User account is already linked to another employee",
            )

    if "role" in update_data or "license_number" in update_data:
        final_role = update_data.get("role", employee.role)
        final_license = update_data.get(
            "license_number",
            employee.license_number,
        )

        if final_role == WorkforceRole.DRIVER.value and not final_license:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driving license number is required for drivers",
            )

        if (
            final_role != WorkforceRole.DRIVER.value
            and final_license
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only drivers can have driving license details",
            )

    return update_employee(db, employee, update_data)


def update_employee_status(
    db: Session,
    employee_id: int,
    new_status: WorkforceStatus,
):
    employee = get_employee_details(db, employee_id)

    if employee.status == WorkforceStatus.ASSIGNED.value:
        if new_status in {
            WorkforceStatus.INACTIVE,
            WorkforceStatus.ON_LEAVE,
        }:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned employees cannot be deactivated or placed on leave",
            )

    return update_employee(
        db,
        employee,
        {"status": new_status.value},
    )


def remove_employee(db: Session, employee_id: int):
    employee = get_employee_details(db, employee_id)

    if employee.status in {
        WorkforceStatus.ASSIGNED.value,
        WorkforceStatus.ON_DUTY.value,
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assigned or on-duty employees cannot be deleted",
        )

    delete_employee(db, employee)

    return {
        "message": "Employee deleted successfully",
        "employee_id": employee_id,
    }