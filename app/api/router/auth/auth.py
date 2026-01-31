from fastapi import APIRouter, status, Request
from app.core.database import get_db
from app.schemas.auth.login import LoginRequest
from app.service.login_ekak import login_user


from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request):
    """
    Stateless JWT logout.
    Client is responsible for deleting tokens.
    """
    auth_header = request.headers.get("Authorization")

    # Token is optional – logout should always succeed
    if auth_header:
        # Optional: log logout event for audit
        pass

    return {
        "success": True,
        "message": "Logged out successfully"
    }


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    return await login_user(request, db)