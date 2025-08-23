# api/router.py

from fastapi import APIRouter
from database.views import router as db_router
from .search.views import router as search_router
from .user.views import router as user_router
from .post.views import router as post_router


api_router = APIRouter()
api_router.include_router(db_router)
api_router.include_router(search_router)
api_router.include_router(user_router)
api_router.include_router(post_router)

