from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt
from uuid import UUID

from api.user import models, schemas
from api.user.auth import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM
)
from database.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

security = HTTPBearer()


# ------------------- Register User -------------------
@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    """
    try:
        # Check if email already exists
        result = await db.execute(select(models.User).where(models.User.email == user.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Check if username already exists
        result = await db.execute(select(models.User).where(models.User.username == user.username))
        existing_username = result.scalars().first()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")

        # Hash password
        hashed_pw = hash_password(user.password)

        # Create new user
        new_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pw,
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"User creation failed: {str(e)}")


# ------------------- Login User -------------------
@router.post("/login", response_model=schemas.Token)
async def login_user(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user by email and password and return JWT token.
    """
    try:
        result = await db.execute(select(models.User).where(models.User.email == user.email))
        db_user = result.scalars().first()

        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )

        # Create tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": str(db_user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": db_user
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


# ------------------- Get Current User -------------------
@router.get("/me", response_model=schemas.UserResponse)
async def get_user_me(current_user: models.User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user profile: {str(e)}")


# ------------------- Update User Profile (Example protected route) -------------------
@router.put("/me", response_model=schemas.UserResponse)
async def update_user_profile(
    username: str = None,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user's profile.
    """
    try:
        if username and username != current_user.username:
            # Check if new username is already taken
            result = await db.execute(select(models.User).where(models.User.username == username))
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Username already taken")
            
            current_user.username = username
        
        await db.commit()
        await db.refresh(current_user)
        return current_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update user profile: {str(e)}")


# ------------------- Refresh Token -------------------
@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    """
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type")
            
            if user_id is None or token_type != "refresh":
                raise credentials_exception
                
        except JWTError:
            raise credentials_exception
        
        # Get user from database
        result = await db.execute(select(models.User).where(models.User.id == UUID(user_id)))
        user = result.scalars().first()
        
        if user is None:
            raise credentials_exception
        
        # Create new tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token refresh failed: {str(e)}")
