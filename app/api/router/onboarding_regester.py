from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.admin.onboarding import CameraOnboardingRequest
from app.core.auth.dependency import get_current_user
from app.models.user import User
from app.service.admin.onboarding_regester import complete_onboarding

router = APIRouter()

@router.post("/onboarding_register/admin")
async def onboard_admin(
    request: CameraOnboardingRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await complete_onboarding(
        request=request,
        db=db,
        current_user=current_user
    )
