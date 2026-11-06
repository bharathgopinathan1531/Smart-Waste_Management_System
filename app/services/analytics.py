
from datetime import date, datetime, time, timedelta

from app.models.collection import CollectionRecord
from app.models.assignment import CollectionAssignment
from app.utils.enums import AssignmentStatus


def get_collection_performance(
    db,
    start_date: date,
    end_date: date,
):
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")

    start_datetime = datetime.combine(start_date, time.min)
    end_datetime = datetime.combine(
        end_date + timedelta(days=1),
        time.min,
    )

    # Fetch assignments created within the requested date range.
    assignments = (
        db.query(CollectionAssignment)
        .filter(
            CollectionAssignment.assigned_at >= start_datetime,
            CollectionAssignment.assigned_at < end_datetime,
        )
        .all()
    )

    total_collections = len(assignments)

    completed_assignments = [
        assignment
        for assignment in assignments
        if assignment.status == AssignmentStatus.COMPLETED
    ]

    completed_count = len(completed_assignments)

    pending_count = sum(
        1
        for assignment in assignments
        if assignment.status in (
            AssignmentStatus.ASSIGNED,
            AssignmentStatus.IN_PROGRESS,
        )
    )

    missed_count = sum(
        1
        for assignment in assignments
        if str(assignment.status).lower()
        in ("missed", "assignmentstatus.missed")
    )

    # Fetch collection records completed within the requested date range.
    collection_records = (
        db.query(CollectionRecord)
        .filter(
            CollectionRecord.collection_completed_at >= start_datetime,
            CollectionRecord.collection_completed_at < end_datetime,
        )
        .all()
    )

    total_quantity = sum(
        float(record.collected_quantity or 0)
        for record in collection_records
    )

    average_quantity = (
        total_quantity / len(collection_records)
        if collection_records
        else 0
    )

    completion_rate = (
        completed_count / total_collections * 100
        if total_collections
        else 0
    )

    # Daily performance.
    daily_data = {}

    def get_daily_entry(day):
        if day not in daily_data:
            daily_data[day] = {
                "total_collections": 0,
                "completed_collections": 0,
                "total_quantity_collected": 0.0,
            }

        return daily_data[day]

    for assignment in assignments:
        day = assignment.assigned_at.date().isoformat()
        entry = get_daily_entry(day)

        entry["total_collections"] += 1

        if assignment.status == AssignmentStatus.COMPLETED:
            entry["completed_collections"] += 1

    for record in collection_records:
        day = record.collection_completed_at.date().isoformat()
        entry = get_daily_entry(day)

        entry["total_quantity_collected"] += float(
            record.collected_quantity or 0
        )

    # Driver performance.
    driver_data = {}

    for assignment in assignments:
        driver = assignment.driver

        if not driver:
            continue

        driver_id = driver.id

        if driver_id not in driver_data:
            driver_data[driver_id] = {
                "driver_id": driver_id,
                "driver_name": driver.full_name,
                "total_assignments": 0,
                "completed_assignments": 0,
                "total_quantity_collected": 0.0,
            }

        driver_data[driver_id]["total_assignments"] += 1

        if assignment.status == AssignmentStatus.COMPLETED:
            driver_data[driver_id]["completed_assignments"] += 1

    for record in collection_records:
        assignment = record.assignment

        if not assignment or not assignment.driver:
            continue

        driver_id = assignment.driver.id

        if driver_id in driver_data:
            driver_data[driver_id]["total_quantity_collected"] += float(
                record.collected_quantity or 0
            )

    driver_performance = []

    for data in driver_data.values():
        total = data["total_assignments"]
        completed = data["completed_assignments"]

        driver_performance.append({
            **data,
            "completion_rate": round(
                completed / total * 100 if total else 0,
                2,
            ),
            "total_quantity_collected": round(
                data["total_quantity_collected"],
                2,
            ),
        })

    # Vehicle performance.
    vehicle_data = {}

    for assignment in assignments:
        vehicle = assignment.vehicle

        if not vehicle:
            continue

        vehicle_id = vehicle.id

        if vehicle_id not in vehicle_data:
            vehicle_data[vehicle_id] = {
                "vehicle_id": vehicle_id,
                "registration_number": vehicle.registration_number,
                "total_assignments": 0,
                "completed_assignments": 0,
                "total_quantity_collected": 0.0,
            }

        vehicle_data[vehicle_id]["total_assignments"] += 1

        if assignment.status == AssignmentStatus.COMPLETED:
            vehicle_data[vehicle_id]["completed_assignments"] += 1

    for record in collection_records:
        assignment = record.assignment

        if not assignment or not assignment.vehicle:
            continue

        vehicle_id = assignment.vehicle.id

        if vehicle_id in vehicle_data:
            vehicle_data[vehicle_id]["total_quantity_collected"] += float(
                record.collected_quantity or 0
            )

    vehicle_performance = [
        {
            **data,
            "total_quantity_collected": round(
                data["total_quantity_collected"],
                2,
            ),
        }
        for data in vehicle_data.values()
    ]

    return {
        "start_date": start_date,
        "end_date": end_date,
        "summary": {
            "total_collections": total_collections,
            "completed_collections": completed_count,
            "pending_collections": pending_count,
            "missed_collections": missed_count,
            "total_quantity_collected": round(total_quantity, 2),
            "average_quantity_per_collection": round(
                average_quantity,
                2,
            ),
            "completion_rate": round(completion_rate, 2),
        },
        "daily_performance": [
            {
                "period": day,
                **values,
                "total_quantity_collected": round(
                    values["total_quantity_collected"],
                    2,
                ),
            }
            for day, values in sorted(daily_data.items())
        ],
        "driver_performance": driver_performance,
        "vehicle_performance": vehicle_performance,
    }
