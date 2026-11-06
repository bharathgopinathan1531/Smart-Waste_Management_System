Writing
Smart Waste Management & Recycling Operations System
Advanced FastAPI Backend Development Project – 5-Day Implementation
� � � � � � �
1. Project Overview
The Smart Waste Management & Recycling Operations System is a production-oriented backend application developed using FastAPI and Python.
The system is designed to manage waste collection operations, collection vehicles, drivers, pickup requests, recycling centers, waste segregation, processing activities, disposal records, route assignments, customer complaints, and environmental impact reports.
The primary objective is to help waste management organizations improve operational efficiency, monitor collection activities, optimize resource allocation, maintain accurate waste inventory records, and measure recycling performance.
The application provides role-based access control, secure authentication, workflow validation, database transaction management, analytics, reporting, and administrative dashboards.
2. Project Objectives
Automate waste collection operations.
Manage customer pickup requests.
Track collection vehicles and workforce.
Assign drivers and field workers.
Monitor waste collection activities.
Manage recycling centers and waste transfers.
Track waste segregation and recycling processes.
Maintain disposal records.
Monitor vehicle maintenance.
Manage customer complaints.
Calculate environmental impact.
Generate operational reports.
Provide administrative dashboards.
Maintain audit logs and system security.
3. Technology Stack
Technology
Purpose
Python 3.11+
Backend programming
FastAPI
REST API development
Pydantic
Request validation and serialization
SQLAlchemy 2.0
Database ORM
PostgreSQL / MySQL
Relational database
JWT
Authentication
Argon2
Password hashing
Alembic
Database migrations
Pytest
Automated testing
Docker
Application containerization
Docker Compose
Multi-container deployment
Swagger / OpenAPI
API documentation
Redis
Optional caching
Celery
Optional background processing
4. User Roles
The system supports seven roles.
Super Admin
Complete system administration.
User and role management.
System configuration.
Administrative approvals.
Audit log access.
Operations Manager
Manage collection operations.
Monitor vehicles and workforce.
Manage operational schedules.
View performance reports.
Collection Supervisor
Manage collection assignments.
Monitor collection activities.
Assign drivers and field workers.
Track missed pickups.
Driver
View assigned collection schedules.
Update collection status.
Record collected quantities.
Submit collection remarks.
Recycling Center Manager
Manage recycling center operations.
Receive transferred waste.
Monitor processing activities.
Approve disposal activities according to permissions.
Field Worker
Assist with waste collection.
Record segregation activities.
Update field operations.
Submit operational information.
Customer
Register and manage profile.
Create pickup requests.
Track collection status.
Submit service complaints.
All protected operations must enforce server-side role permissions.
5. Five-Day Development Roadmap
DAY 1 – Authentication, Locations & Waste Management
Level 1 – Authentication & Authorization
Features:
User registration and login.
JWT access and refresh tokens.
Password hashing.
Role-based access control.
User activation and deactivation.
Password reset workflow.
Protected APIs.
Current-user API.
Security requirements:
Secure password storage.
Access-token expiration.
Refresh-token rotation and revocation.
Single-use password reset tokens.
Role validation.
Inactive account restrictions.
Level 2 – Location Management
Features:
Register service zones.
Create collection areas.
Add streets and localities.
Assign supervisors.
Configure collection schedules.
Track zone status.
Zone-wise search and filtering.
Level 3 – Waste Category Management
Waste categories:
Organic Waste.
Plastic Waste.
Paper Waste.
Metal Waste.
Glass Waste.
Electronic Waste.
Hazardous Waste.
Features:
Category creation.
Waste classification.
Segregation rules.
Recyclability status.
Disposal instructions.
Level 4 – Customer Management
Features:
Customer registration.
Customer address management.
Customer location mapping.
Customer service status.
Collection history.
Customer search and filtering.
Day 1 Deliverable: Authentication, location, waste category, and customer management APIs.
DAY 2 – Collection Requests, Vehicles & Workforce
Level 5 – Waste Pickup Requests
Features:
Create pickup requests.
Select waste category.
Estimated waste quantity.
Pickup address.
Preferred pickup date.
Request priority.
Pickup status tracking.
Request cancellation.
Pickup statuses:
Pending.
Approved.
Assigned.
Scheduled.
Collected.
Cancelled.
Rejected.
Level 6 – Vehicle Management
Features:
Register collection vehicles.
Vehicle registration number.
Vehicle type.
Capacity.
Fuel type.
Vehicle status.
Maintenance records.
Vehicle availability.
Business validations:
Prevent assigning unavailable vehicles.
Prevent assignments exceeding vehicle capacity.
Prevent duplicate vehicle registration numbers.
Level 7 – Driver & Worker Management
Features:
Driver registration.
Worker registration.
License details.
Skills.
Contact information.
Availability status.
Supervisor assignment.
Workforce history.
Level 8 – Collection Assignment
Features:
Assign pickup requests.
Assign drivers.
Assign vehicles.
Assign field workers.
Set collection schedules.
Reassign pending collections.
Track assignment history.
Business validations:
Validate vehicle capacity.
Validate driver availability.
Validate worker availability.
Prevent conflicting assignments.
Level 9 – Collection Tracking
Features:
Start collection.
Record collected quantity.
Collection timestamp.
Collection status.
Field remarks.
Upload photo reference URLs.
Record incomplete pickups.
Collection history.
Day 2 Deliverable: Pickup request workflow, vehicle management, workforce, assignment, and collection tracking APIs.
DAY 3 – Recycling Center & Processing Management
Level 10 – Recycling Center Management
Features:
Register recycling centers.
Center location.
Processing capacity.
Accepted waste categories.
Center availability.
Manager assignment.
Center status.
Level 11 – Waste Transfer Management
Features:
Transfer collected waste to centers.
Create transfer records.
Source location.
Destination center.
Waste category.
Transfer quantity.
Vehicle assignment.
Transfer status.
Transfer history.
Level 12 – Waste Segregation
Features:
Record incoming waste.
Segregate waste by category.
Record recyclable quantity.
Record non-recyclable quantity.
Record contaminated waste.
Maintain segregation history.
Business validations:
Prevent negative quantities.
Ensure segregated quantities reconcile with received quantities.
Maintain traceability of waste movements.
Level 13 – Recycling Processing
Features:
Create processing batches.
Assign waste categories.
Record input quantity.
Record recycled output quantity.
Record processing loss.
Processing date.
Processing status.
Calculate recycling yield percentage.
Formula:
Recycling Yield (%) = (Recycled Output Quantity / Input Quantity) × 100
Processing loss = Input Quantity − Recycled Output Quantity.
Level 14 – Disposal Management
Features:
Create disposal records.
Disposal method.
Waste quantity.
Disposal location.
Disposal date.
Responsible person.
Disposal approval.
Disposal history.
Day 3 Deliverable: Recycling center, waste transfer, segregation, processing, and disposal APIs.
DAY 4 – Maintenance, Complaints & Operational Analytics
Level 15 – Vehicle Maintenance
Features:
Maintenance requests.
Preventive maintenance schedules.
Breakdown reports.
Maintenance cost.
Technician assignment.
Vehicle downtime.
Maintenance history.
Level 16 – Customer Complaints
Features:
Create complaints.
Complaint category.
Complaint description.
Priority.
Assign responsible team.
Complaint status.
Resolution remarks.
Complaint history.
Level 17 – Collection Performance
Performance metrics:
Total pickup requests.
Completed pickups.
Missed pickups.
Average collection time.
Zone-wise collection performance.
Driver-wise collection performance.
Vehicle utilization.
Collection efficiency.
Example formulas:
Collection Completion Rate (%) = (Completed Pickups / Eligible Pickup Requests) × 100
Collection Efficiency (%) = (Successful Pickups / Scheduled Pickups) × 100
Average Collection Time = Total Collection Duration / Number of Completed Collections.
Level 18 – Environmental Impact Tracking
Metrics:
Total waste collected.
Total recyclable waste.
Total waste recycled.
Total waste disposed.
Recycling percentage.
Waste category distribution.
Monthly recycling trends.
Calculation formulas:
Recycling Percentage (%) = (Total Recycled Waste / Total Waste Collected) × 100
Disposal Percentage (%) = (Total Waste Disposed / Total Waste Collected) × 100
Waste Remaining = Total Waste Collected − Total Waste Accounted For.
All metrics must use consistent units, date ranges, and waste accounting rules. Avoid double-counting waste during transfers between locations.
Level 19 – Notifications
Generate notifications for:
New pickup requests.
Collection assignments.
Missed collections.
Vehicle breakdowns.
Maintenance due.
Center capacity alerts.
Customer complaints.
Pending approvals.
Day 4 Deliverable: Maintenance, complaints, analytics, environmental metrics, and notifications.
DAY 5 – Dashboard, Reports, Testing & Deployment
Level 20 – Admin Dashboard
Dashboard APIs:
Total customers.
Total collection requests.
Completed collections.
Pending pickups.
Missed collections.
Total vehicles.
Available vehicles.
Active recycling centers.
Total waste collected.
Total waste recycled.
Recycling efficiency.
Pending complaints.
Vehicle maintenance status.
Level 21 – Advanced Reports
Reports:
Daily collection reports.
Monthly collection reports.
Zone-wise performance.
Driver performance.
Vehicle utilization.
Waste category reports.
Recycling center performance.
Recycling yield reports.
Disposal reports.
Environmental impact reports.
Supported functionality:
Date-range filtering.
Zone filtering.
Waste category filtering.
Status filtering.
Pagination.
Sorting.
CSV export.
Level 22 – Audit Logs
Track:
User login.
Pickup creation.
Assignment changes.
Collection completion.
Waste transfer.
Segregation records.
Processing records.
Disposal approvals.
Vehicle maintenance.
Administrative changes.
Audit records must store:
Actor.
Action.
Entity.
Entity identifier.
Timestamp.
Relevant change details.
Level 23 – Security & Validation
Features:
JWT authentication.
Role-based permissions.
Pydantic validation.
Duplicate prevention.
Global exception handling.
Database transactions.
Proper HTTP status codes.
Database indexing.
Soft delete.
Secure environment configuration.
Additional security practices:
Secure secret management.
Password hashing.
Input validation.
Protection against unauthorized access.
Safe database transaction handling.
Token expiration and revocation.
Level 24 – Testing & Deployment
Testing requirements:
Authentication tests.
Role permission tests.
Pickup request creation tests.
Vehicle assignment tests.
Capacity validation tests.
Collection tracking tests.
Waste transfer tests.
Recycling calculation tests.
Disposal approval tests.
Dashboard metric tests.
Deployment deliverables:
Dockerfile.
Docker Compose.
Alembic migrations.
requirements.txt.
.env.example.
README.md.
Swagger documentation.
Postman collection.
Unit and integration tests.
Day 5 Deliverable: Complete backend testing, deployment configuration, documentation, and end-to-end validation.
6. Recommended Project Architecture
Smart_Waste_Management_Recycling_Operations_System/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── customers.py
│   │       │   ├── locations.py
│   │       │   ├── waste_categories.py
│   │       │   ├── pickup_requests.py
│   │       │   ├── vehicles.py
│   │       │   ├── drivers.py
│   │       │   ├── workers.py
│   │       │   ├── assignments.py
│   │       │   ├── collections.py
│   │       │   ├── recycling_centers.py
│   │       │   ├── waste_transfers.py
│   │       │   ├── segregation.py
│   │       │   ├── processing.py
│   │       │   ├── disposal.py
│   │       │   ├── maintenance.py
│   │       │   ├── complaints.py
│   │       │   ├── analytics.py
│   │       │   ├── notifications.py
│   │       │   ├── dashboard.py
│   │       │   ├── reports.py
│   │       │   └── audit_logs.py
│   │       └── router.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   └── permissions.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── db/
│   ├── middleware/
│   ├── utils/
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/
├── postman/
├── screenshots/
│
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
The architecture is modular. Each business domain should have its own models, schemas, services, repositories, and API endpoints as the project grows.
7. Database Design
The database will contain related entities for authentication, customers, locations, collection operations, vehicles, workforce, recycling, disposal, and analytics.
Core database entities
Module
Main Entities
Authentication
Users, Refresh Tokens, Password Reset Tokens
Locations
Zones, Collection Areas, Streets, Schedules
Waste
Waste Categories, Segregation Rules
Customers
Customers, Customer Addresses
Pickup
Pickup Requests
Vehicles
Vehicles, Maintenance Records
Workforce
Drivers, Workers, Skills
Assignment
Collection Assignments
Tracking
Collection Records
Recycling
Recycling Centers
Transfer
Waste Transfers
Segregation
Segregation Records
Processing
Processing Batches
Disposal
Disposal Records
Complaints
Customer Complaints
Notifications
Notifications
Audit
Audit Logs
Database design principles
Use primary keys and foreign keys.
Enforce unique constraints.
Use appropriate indexes.
Maintain referential integrity.
Use database transactions for critical operations.
Prevent negative inventory and waste quantities.
Maintain accurate quantity records.
Use soft deletion where appropriate.
Track creation and modification timestamps.
An ER diagram should be maintained as the database expands.
8. API Documentation
FastAPI automatically generates interactive API documentation.
After starting the application:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
Health Check: http://127.0.0.1:8000/health
API endpoints should follow a consistent versioned structure:
/api/v1/auth
/api/v1/users
/api/v1/customers
/api/v1/locations
/api/v1/waste-categories
/api/v1/pickup-requests
/api/v1/vehicles
/api/v1/drivers
/api/v1/workers
/api/v1/assignments
/api/v1/collections
/api/v1/recycling-centers
/api/v1/waste-transfers
/api/v1/segregation
/api/v1/processing
/api/v1/disposal
/api/v1/maintenance
/api/v1/complaints
/api/v1/analytics
/api/v1/notifications
/api/v1/dashboard
/api/v1/reports
/api/v1/audit-logs
9. Mandatory End-to-End Workflow
The system must support the following complete business workflow:
Admin Login
    |
    v
Create Collection Zone
    |
    v
Register Customer
    |
    v
Create Pickup Request
    |
    v
Assign Vehicle
    |
    v
Assign Driver
    |
    v
Complete Collection
    |
    v
Transfer Waste
    |
    v
Receive at Recycling Center
    |
    v
Segregate Waste
    |
    v
Process Recycling Batch
    |
    v
Record Disposal
    |
    v
Calculate Environmental Impact
    |
    v
View Admin Dashboard
    |
    v
Generate Reports
    |
    v
Verify Audit Logs
Each step must validate the preceding operation and maintain accurate database records.
The end-to-end workflow must also be covered by automated integration tests.
10. Business Logic & Validation
The application must enforce business rules instead of relying only on CRUD operations.
Vehicle assignment
Vehicle must be available.
Vehicle capacity must support the assigned collection.
Driver must be available.
Assigned workforce must not have conflicting schedules.
Pickup requests
Pickup quantity must be positive.
Pickup date must be valid.
Cancelled or rejected requests cannot be collected.
Collection completion must record the actual collected quantity.
Waste transfer
Transfer quantity must not exceed the available collected quantity.
Destination center must be active.
Accepted waste category must be supported.
Transfer status must follow a valid workflow.
Waste segregation
All quantities must be non-negative.
Segregated quantities must reconcile with incoming quantities, accounting for explicitly recorded discrepancies.
Recycling processing
Output quantity cannot exceed input quantity.
Processing loss must be calculated correctly.
Recycling yield must be calculated consistently.
Disposal
Disposal quantities must be validated against available waste.
Required approvals must be enforced.
Disposal records must maintain traceability.
Database consistency
Use transactions for critical business operations.
Prevent duplicate records.
Maintain accurate inventory.
Avoid partial updates when an operation fails.
11. Environmental Impact Calculations
The application will calculate environmental performance using recorded waste quantities.
Total waste collected
Sum of successfully recorded collection quantities for the selected period.
Total waste recycled
Sum of accepted recycled output quantities from completed processing batches.
Recycling efficiency
Recycling Efficiency (%) =
(Total Recycled Quantity / Total Waste Collected) × 100
Waste disposal percentage
Disposal Percentage (%) =
(Total Disposed Quantity / Total Waste Collected) × 100
Vehicle utilization
Vehicle Utilization (%) =
(Actual Operating Hours / Available Operating Hours) × 100
Important assumptions
All waste quantities must use consistent measurement units.
Transfers between centers must not be counted as new waste collection.
Recycled quantities must be calculated from completed processing records.
Reprocessing must not double-count the same material.
Reports must support defined date ranges.
Zero denominators must be handled safely.
12. Testing Strategy
Testing will be performed using Pytest and FastAPI TestClient.
Unit testing
Test individual business logic components:
Password hashing.
Token generation.
Permission validation.
Waste quantity calculations.
Recycling yield calculations.
Collection efficiency calculations.
Input validation.
Integration testing
Test complete API workflows:
User registration and login.
Protected endpoints.
Role-based permissions.
Pickup request creation.
Vehicle assignment.
Collection completion.
Waste transfer.
Segregation.
Recycling processing.
Disposal approval.
Dashboard metrics.
Audit log generation.
Negative testing
Verify that the application correctly rejects:
Invalid credentials.
Expired tokens.
Inactive users.
Unauthorized roles.
Duplicate registrations.
Negative quantities.
Vehicle capacity violations.
Unavailable vehicle assignments.
Invalid status transitions.
Invalid disposal approvals.
Run tests
pytest -v
Run with coverage:
pip install pytest-cov

pytest --cov=app --cov-report=term-missing
13. Installation & Setup
Prerequisites
Install:
Python 3.11 or higher.
Visual Studio Code.
PostgreSQL or MySQL.
Git.
Docker Desktop (optional).
Step 1 – Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL
cd Smart_Waste_Management_Recycling_Operations_System
Step 2 – Create virtual environment
Windows:
py -3.11 -m venv venv
Activate:
.\venv\Scripts\Activate.ps1
Step 3 – Install dependencies
python -m pip install --upgrade pip

pip install -r requirements.txt
Step 4 – Configure environment
Create .env from .env.example.
Configure:
APP_NAME=Smart Waste Management System
ENVIRONMENT=development

DATABASE_URL=sqlite:///./smart_waste.db

JWT_SECRET_KEY=YOUR_SECURE_SECRET_KEY
JWT_ALGORITHM