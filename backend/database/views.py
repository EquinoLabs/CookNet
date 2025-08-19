from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from database.database import get_db

router = APIRouter(prefix="/db_query", tags=["database"])


@router.get("/tables", response_model=list[str])
async def get_table_names(db: AsyncSession = Depends(get_db)):
    """
    Retrieve the names of all user-defined tables in the database.
    """
    query = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    result = await db.execute(query)
    tables = result.scalars().all()
    return tables

@router.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"result": result.scalar_one()}
