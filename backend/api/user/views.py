from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from api.user import models, schemas
from database.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ------------------- Register User -------------------
@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    """
    # Check if email already exists
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

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


# ------------------- Login User -------------------
@router.post("/login", response_model=schemas.UserResponse)
async def login_user(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user by email and password.
    """
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    db_user = result.scalars().first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return db_user
