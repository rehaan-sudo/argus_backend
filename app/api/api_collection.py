from fastapi import APIRouter
from app.api.router.regester import router as user
from app.api.router.onboarding_regester import router as onboarding

api_router = APIRouter()
api_router.include_router(user, prefix="/users", tags=["Users"])
api_router.include_router(onboarding, prefix="/onboarding", tags=["Onboarding"])