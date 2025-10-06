from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.user import UserPublic, UserUpdate
from app.services import user_service
from app.services.security import get_current_active_user

router = APIRouter()

@router.get("/{user_id}", response_model=UserPublic)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserPublic = Depends(get_current_active_user)
):
    """Get a specific user by ID."""
    user = await user_service.get(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.put("/me", response_model=UserPublic)
async def update_user_me(
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserPublic = Depends(get_current_active_user)
):
    """Update the current user's information."""
    user = await user_service.get(db, user_id=current_user.id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    updated_user = await user_service.update(db, db_user=user, user_in=user_in)
    return updated_user
