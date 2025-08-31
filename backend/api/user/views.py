import os
import httpx
import secrets
import string
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
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
    ALGORITHM,
    send_verification_email_service
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
        # Always force role = user here for safety
        role = schemas.RoleEnum.user

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
            role=role,
            is_email_verified=False,
            verification_email_sent=False
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        # Automatically send verification email
        try:
            verification_token = create_access_token(
                data={"sub": str(new_user.id), "type": "email_verification"},
                expires_delta=timedelta(hours=24)
            )
            await send_verification_email_service(new_user.email, new_user.username, verification_token)
            
            new_user.verification_email_sent = True
            await db.commit()

        except Exception as e:
            print(f"⚠️ Failed to send verification email: {e}")

        return new_user
    except HTTPException as e:
        raise e
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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")


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


@router.post("/register-role", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user_with_role(
    user: schemas.UserCreateWithRole,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # require auth
):
    """
    Register a new user with a specific role (admin/owner/moderator).
    Only admins/owners can access this.
    """
    try:
        # Check if role is admin or owner
        if current_user.role not in [schemas.RoleEnum.admin, schemas.RoleEnum.owner]:
            raise HTTPException(status_code=403, detail="Not authorized to create role-based users")

        # Reuse same duplicate checks
        result = await db.execute(select(models.User).where(models.User.email == user.email))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Email already registered")

        result = await db.execute(select(models.User).where(models.User.username == user.username))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Username already taken")

        # Hash password
        hashed_pw = hash_password(user.password)

        # Create new user with role
        new_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pw,
            role=user.role
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create role-based user: {str(e)}")


@router.post("/google-login", response_model=schemas.Token)
async def google_login(request: schemas.GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user using Google OAuth token.
    """
    try:
        # Verify Google ID token
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={request.token}"
            )
            
            if response.status_code != 200:
                print(f"Google verification failed: {response.text}")
                raise HTTPException(status_code=400, detail="Invalid Google token")
            
            token_info = response.json()
            
            # Verify token is for your app
            google_client_id = os.getenv("GOOGLE_CLIENT_ID")
            if token_info.get('aud') != google_client_id:
                raise HTTPException(status_code=400, detail="Token not for this application")

        # Extract user info from verified token
        google_id = token_info['sub']
        email = token_info['email']
        name = token_info.get('name', '')
        picture = token_info.get('picture', '')

        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by Google")

        # Check if user exists by email OR google_id
        result = await db.execute(
            select(models.User).where(
                or_(models.User.email == email, models.User.google_id == google_id)
            )
        )
        user = result.scalars().first()
        
        if user:
            # Update existing user with Google info if needed
            if not user.google_id:
                user.google_id = google_id
            if picture and not user.profile_image:  # Using your existing field name
                user.profile_image = picture
            if not user.is_email_verified:
                user.is_email_verified = True
            
            await db.commit()
            await db.refresh(user)
        else:
            # Create new user
            # Generate unique username from name or email
            base_username = name.replace(" ", "").lower() if name else email.split("@")[0]
            username = base_username
            
            # Ensure username is unique
            counter = 1
            while True:
                result = await db.execute(
                    select(models.User).where(models.User.username == username)
                )
                if not result.scalars().first():
                    break
                username = f"{base_username}{counter}"
                counter += 1

            # Create new user
            user = models.User(
                username=username,
                email=email,
                hashed_password=hash_password(generate_random_password()),
                google_id=google_id,
                profile_image=picture,  # Using your existing field name
                is_email_verified=True,
                role=schemas.RoleEnum.user.value  # Default role
            )
            
            db.add(user)
            await db.commit()
            await db.refresh(user)

        # Create tokens (same pattern as your login endpoint)
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

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"Google auth error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error during Google authentication: {str(e)}")


def generate_random_password():
    """Generate random password for Google users"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for i in range(16))


@router.post("/send-verification-email")
async def send_verification_email(
    request: schemas.ResendVerificationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Send verification email to user.
    """
    try:
        # Find user by email
        result = await db.execute(select(models.User).where(models.User.email == request.email))
        user = result.scalars().first()
        
        if not user:
            # Don't reveal if email exists or not for security
            return {"message": "If email exists, verification email sent"}
        
        if user.is_email_verified:
            raise HTTPException(status_code=400, detail="Email already verified")
        
        # Create verification token (expires in 24 hours)
        verification_token = create_access_token(
            data={"sub": str(user.id), "type": "email_verification"},
            expires_delta=timedelta(hours=24)
        )
        
        # Send email (implement based on your email service)
        await send_verification_email_service(user.email, user.username, verification_token)
        
        return {"message": "Verification email sent"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Send verification email error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send verification email")


@router.get("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    Verify user's email using verification token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if not user_id or token_type != "email_verification":
            raise HTTPException(status_code=400, detail="Invalid verification token")
        
        result = await db.execute(select(models.User).where(models.User.id == UUID(user_id)))
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.is_email_verified:
            raise HTTPException(status_code=400, detail="Email already verified")
        
        user.is_email_verified = True
        await db.commit()
        await db.refresh(user)
        
        return {"message": "Email verified successfully"}
    
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    except Exception as e:
        await db.rollback()
        print(f"Email verification error: {e}")
        raise HTTPException(status_code=500, detail=f"Email verification failed: {e}")
