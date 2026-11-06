
from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.locations import router as locations_router
from app.api.v1.endpoints import waste_categories
from app.api.v1.endpoints import customers
from app.api.v1.endpoints import pickup_requests
from app.api.v1.endpoints import vehicles
from app.api.v1.endpoints import workforce
from app.api.v1.endpoints import assignments
from app.api.v1.endpoints import collections
from app.api.v1.endpoints import recycling_centers
from app.api.v1.endpoints import transfers
from app.api.v1.endpoints import segregation
from app.api.v1.endpoints import processing
from app.api.v1.endpoints import disposal
from app.api.v1.endpoints import maintenance
from app.api.v1.endpoints import complaints
from app.api.v1.endpoints import analytics
from app.api.v1.endpoints import environmental_impact
from app.api.v1.endpoints import notifications
from app.api.v1.endpoints import dashboard
from app.api.v1.endpoints import reports
from app.api.v1.endpoints import audit_logs
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Smart Waste Management and Recycling Operations System"
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(locations_router, prefix="/api/v1")
app.include_router(waste_categories.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")
app.include_router(pickup_requests.router, prefix="/api/v1")
app.include_router(vehicles.router, prefix="/api/v1")
app.include_router(workforce.router, prefix="/api/v1")
app.include_router(assignments.router, prefix="/api/v1")
app.include_router(collections.router, prefix="/api/v1")
app.include_router(recycling_centers.router, prefix="/api/v1")
app.include_router(transfers.router, prefix="/api/v1")
app.include_router(segregation.router, prefix="/api/v1")
app.include_router(processing.router, prefix="/api/v1")
app.include_router(disposal.router, prefix="/api/v1")
app.include_router(maintenance.router, prefix="/api/v1")
app.include_router(complaints.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(environmental_impact.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(audit_logs.router, prefix="/api/v1")
app.add_middleware(SecurityHeadersMiddleware)

@app.get("/")
def root():
    return {
        "message": "Smart Waste Management API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
app.add_middleware(
    RateLimitMiddleware,
    max_requests=100,
    window_seconds=60,
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(str(part) for part in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Request validation failed",
            "errors": errors,
        },
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
