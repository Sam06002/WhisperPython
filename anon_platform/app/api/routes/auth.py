from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.schemas.user import Token, UserCreate, UserPublic
from app.services import user_service
from app.services.security import (
    create_access_token,
    get_current_active_user,
    get_password_hash,
)

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """OAuth2 compatible token login, get an access token for future requests."""
    user = await user_service.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserPublic)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    # Check if username is already taken
    existing_user = await user_service.get_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # Create new user
    user = await user_service.create(db, user_in=user_in)
    return user

@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: UserPublic = Depends(get_current_active_user)
):
    """Get current user."""
    return current_user

@router.get("/register/generate-username", response_model=dict)
async def generate_username(db: AsyncSession = Depends(get_db)):
    """Generate a unique random username."""
    username = await user_service.get_unique_random_username(db)
    return {"username": username}
