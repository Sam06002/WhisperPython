from typing import Optional, List
import names
import random
import string
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.user import UserCreate, UserInDB, UserUpdate, UserPublic
from app.services.security import get_password_hash, verify_password

class UserService:
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get a user by username."""
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()
    
    @staticmethod
    async def get(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return await db.get(User, user_id)
    
    @staticmethod
    async def create(db: AsyncSession, user_in: UserCreate) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            username=user_in.username,
            hashed_password=hashed_password,
            bio=user_in.bio,
            avatar_url=user_in.avatar_url,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def update(
        db: AsyncSession, db_user: User, user_in: UserUpdate
    ) -> User:
        """Update a user."""
        update_data = user_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def authenticate(
        db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        """Authenticate a user."""
        user = await UserService.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    async def get_unique_random_username(db: AsyncSession) -> str:
        """Generate a unique random username."""
        while True:
            # Generate a random name
            first_name = names.get_first_name().lower()
            random_suffix = ''.join(random.choices(string.digits, k=4))
            username = f"{first_name}{random_suffix}"
            
            # Check if username exists
            existing_user = await UserService.get_by_username(db, username)
            if not existing_user:
                return username

# Create an instance of the service
user_service = UserService()
