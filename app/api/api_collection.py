from fastapi import APIRouter
from app.api.router.regester import router as user
from app.api.router.onboarding_regester import router as onboarding
from app.api.router.auth.auth import router as auth

api_router = APIRouter()
api_router.include_router(user, prefix="/users", tags=["Users Resgester"])
api_router.include_router(onboarding, prefix="/onboarding", tags=["Onboarding"])
api_router.include_router(auth, prefix="/auth", tags=["Authentication"])