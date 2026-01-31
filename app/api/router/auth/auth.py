from fastapi import APIRouter, status, Request, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth.login import LoginRequest
from app.schemas.auth.refresh import RefreshTokenRequest, RefreshTokenResponse
from app.service.login_ekak import login_user
from app.service.refresh_token import refresh_access_token_by_token
from app.core.auth.security import REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
    response: Response = None
):
    """
    Login endpoint - authenticates user and returns access + refresh tokens
    """
    # perform login and set httpOnly cookie for refresh token
    result = await login_user(request, db)

    # Expecting service to return refreshToken
    refresh_token = result.pop("refreshToken", None)

    if not refresh_token:
        # should not happen, but guard
        return result

    # Set httpOnly cookie (max_age in seconds)
    max_age = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    if response is not None:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=max_age,
            path="/"
        )

    return result


@router.post("/refresh", response_model=RefreshTokenResponse, status_code=status.HTTP_200_OK)
async def refresh(
    request: Request,
    db: AsyncSession = Depends(get_db),
    response: Response = None
):
    """
    Refresh token endpoint - exchanges refresh token for new access token.
    Preserves all RBAC information (roleId, organizationId, etc.)
    """
    # read refresh token from httpOnly cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    result = await refresh_access_token_by_token(refresh_token, db)

    # re-set cookie to extend expiration (sliding session) - keep same token unless rotating
    max_age = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    if response is not None:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=max_age,
            path="/"
        )

    return result


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request, response: Response):
    """
    Stateless JWT logout.
    Client is responsible for deleting tokens from local storage.
    """
    auth_header = request.headers.get("Authorization")

    # Token is optional – logout should always succeed
    if auth_header:
        # Optional: log logout event for audit
        pass

    # Clear the httpOnly refresh token cookie
    response.delete_cookie(key="refresh_token", path="/")

    return {
        "success": True,
        "message": "Logged out successfully"
    }
