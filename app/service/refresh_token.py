from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, status
import logging

from app.core.database import get_db
from app.schemas.auth.refresh import RefreshTokenRequest
from app.models.user import User
from app.core.auth.security import verify_token, create_access_token
from app.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


async def refresh_access_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    Validates refresh token and returns new access token with preserved RBAC info.
    """
    try:
        logger.info("Attempting to refresh access token")
        
        # 1️⃣ Verify refresh token validity and type
        payload = verify_token(request.refresh_token, token_type="refresh")
        
        if not payload:
            logger.warning("Invalid or expired refresh token")
            raise ValidationError(message="Invalid or expired refresh token")
        
        # 2️⃣ Extract user ID from token
        user_id = payload.get("userId")
        if not user_id:
            logger.warning("Refresh token missing userId")
            raise ValidationError(message="Invalid token payload")
        
        # 3️⃣ Verify user still exists and is active
        logger.info(f"Verifying user exists: {user_id}")
        result = await db.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalars().first()
        
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise ValidationError(message="User not found")
        
        if user.status != "ACTIVE":
            logger.warning(f"User inactive: {user_id}")
            raise ValidationError(message="User account is not active")
        
        # 4️⃣ Create new access token with same RBAC info
        logger.info(f"Generating new access token for user: {user_id}")
        token_data = {
            "userId": user.user_id,
            "roleId": user.role_id,
            "organizationId": user.organization_id,
            "branchId": user.branch_id,
            "groupId": user.group_id,
            "subGroupId": user.sub_group_id
        }
        
        new_access_token = create_access_token(token_data)
        
        logger.info(f"Access token refreshed successfully for user: {user_id}")
        
        return {
            "success": True,
            "message": "Token refreshed successfully",
            "accessToken": new_access_token,
            "tokenType": "Bearer"
        }
    
    except ValidationError as ve:
        logger.error(f"Validation error during token refresh: {str(ve)}")
        raise ve
    
    except Exception as unexpected_error:
        logger.error(f"Unexpected error during token refresh: {str(unexpected_error)}")
        raise ValidationError(
            message="An unexpected error occurred during token refresh",
        )


async def refresh_access_token_by_token(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Same as `refresh_access_token` but accepts a raw refresh token string (useful when token is stored in cookie).
    Returns dict with accessToken and tokenType (and optionally refreshToken when rotating).
    """
    try:
        logger.info("Attempting to refresh access token (cookie)")

        payload = verify_token(token, token_type="refresh")
        if not payload:
            logger.warning("Invalid or expired refresh token")
            raise ValidationError(message="Invalid or expired refresh token")

        user_id = payload.get("userId")
        if not user_id:
            logger.warning("Refresh token missing userId")
            raise ValidationError(message="Invalid token payload")

        result = await db.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalars().first()

        if not user:
            logger.warning(f"User not found: {user_id}")
            raise ValidationError(message="User not found")

        if user.status != "ACTIVE":
            logger.warning(f"User inactive: {user_id}")
            raise ValidationError(message="User account is not active")

        token_data = {
            "userId": user.user_id,
            "roleId": user.role_id,
            "organizationId": user.organization_id,
            "branchId": user.branch_id,
            "groupId": user.group_id,
            "subGroupId": user.sub_group_id
        }

        new_access_token = create_access_token(token_data)

        logger.info(f"Access token refreshed successfully for user: {user_id}")

        # Return access token; keep refresh token same (cookie stays) unless you implement rotation
        return {
            "success": True,
            "message": "Token refreshed successfully",
            "accessToken": new_access_token,
            "tokenType": "Bearer"
        }

    except ValidationError as ve:
        logger.error(f"Validation error during token refresh: {str(ve)}")
        raise ve

    except Exception as unexpected_error:
        logger.error(f"Unexpected error during token refresh: {str(unexpected_error)}")
        raise ValidationError(
            message="An unexpected error occurred during token refresh",
        )
