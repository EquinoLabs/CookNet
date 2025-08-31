import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from api.user import models, schemas
from database.database import get_db

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))  # Short-lived
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))  # Longer-lived


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token security
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token (supports custom token types)."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Always set expiration
    to_encode.update({"exp": expire})

    # Only set type=access if user didn’t already provide one
    if "type" not in to_encode:
        to_encode["type"] = "access"

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return user ID."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=UUID(user_id))
    except JWTError:
        raise credentials_exception
    
    return token_data.user_id


async def get_current_user(
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
) -> models.User:
    """Get the current authenticated user."""
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


# Email service function (customize based on your email provider)
async def send_verification_email_service(email: str, username: str, token: str):
    verification_url = f"{os.getenv('FRONTEND_URL')}/verify-email?token={token}"
    
    subject = "Verify Your CookNet Email"
    body = f"""
    Hi {username},

    Please verify your email address by clicking the link below:
    {verification_url}

    This link will expire in 24 hours.

    Best regards,
    CookNet Team
    """

    try:
        message = Mail(
            from_email=os.getenv("SENDGRID_SENDER_EMAIL"),
            to_emails=email,
            subject=subject,
            plain_text_content=body
        )

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)

        # Optional: log response details
        print(f"Email sent to {email}, status: {response.status_code}")
        if response.status_code == 202:
            return True
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


# To check email verification for protected routes
def require_verified_email(current_user: models.User = Depends(get_current_user)):
    """
    Dependency to ensure user has verified email for certain endpoints.
    """
    if not current_user.is_email_verified:
        raise HTTPException(
            status_code=403, 
            detail="Email verification required. Please check your email and verify your account."
        )
    return current_user
