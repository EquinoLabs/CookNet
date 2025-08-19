import os
import ssl
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()
load_dotenv()

CONNECTION_NEON_DB = os.getenv("CONNECTION_NEON_DB")
DATABASE_URL = f"postgresql+asyncpg://{CONNECTION_NEON_DB}"

ssl_context = ssl.create_default_context()

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={"ssl": ssl_context}
) # echo for SQL logging
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

if __name__ == '__main__':
    print(DATABASE_URL)
