from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import UserRegister
from app.schemas.users import UserResponse
from app.services.auth import register_user
from app.schemas.auth import RefreshTokenRequest
from app.services.auth import refresh_access_token
from app.schemas.auth import PasswordChangeRequest
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.auth import change_password
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: UserRegister,
    db: Session = Depends(get_db)
):
    return register_user(db, payload)

from app.schemas.auth import UserLogin, TokenResponse
from app.services.auth import login_user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user(
        db,
        payload.email,
        payload.password
    )
@router.post("/refresh")
def refresh_token(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_access_token(
        db,
        payload.refresh_token
    )

@router.post("/change-password")
def update_password(
    payload: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return change_password(
        db,
        current_user,
        payload.current_password,
        payload.new_password
    )