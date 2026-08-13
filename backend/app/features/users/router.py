from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.database import get_db_session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.features.users.models import User
from app.features.users.schemas import Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=True,
        is_superuser=False,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(User).where(User.email == user_credentials.email))
    user = result.scalars().first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    # Return refresh token as well in a real app, keeping it simple here.
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": "dummy-refresh-token"}

@router.post("/logout")
async def logout():
    # Typically handled by frontend deleting the token, but we provide the endpoint.
    return {"message": "Successfully logged out"}

@router.post("/refresh", response_model=Token)
async def refresh_token(db: AsyncSession = Depends(get_db_session)):
    # Placeholder for refresh token logic.
    return {"access_token": "new-access-token", "token_type": "bearer"}

@router.post("/forgot-password")
async def forgot_password(email: str):
    # Placeholder for sending email logic
    return {"message": "If an account with this email exists, a password reset link has been sent."}

@router.post("/reset-password")
async def reset_password(token: str, new_password: str):
    # Placeholder for reset password logic
    return {"message": "Password has been successfully reset."}

from pydantic import BaseModel

from app.api.dependencies import get_current_user


class UserUpdate(BaseModel):
    full_name: str | None = None

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    await db.commit()
    await db.refresh(current_user)
    return current_user
