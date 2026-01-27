from fastapi import APIRouter
from app.api.login.api import router as user

api_router = APIRouter()
api_router.include_router(user, prefix="/users", tags=["Users"])