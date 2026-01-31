from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, status
import logging

from app.core.database import get_db
from app.schemas.auth.login import LoginRequest
from app.models.user import User
from app.core.auth.security import verify_password, create_access_token
from app.core.exceptions import ValidationError, OnboardingError

logger = logging.getLogger(__name__)


async def login_user(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Login attempt for email: {request.email}")

        # 1️⃣ Fetch user by email
        result = await db.execute(
            select(User).where(User.email == request.email)
        )
        user = result.scalars().first()

        # ❌ User not found
        if not user:
            logger.warning(f"Invalid login email: {request.email}")
            raise ValidationError(message="Invalid email or password")

        # ❌ User inactive
        if user.status != "ACTIVE":
            logger.warning(f"Inactive user login attempt: {request.email}")
            raise ValidationError(message="User account is not active")

        # ❌ Password mismatch
        if not verify_password(request.password, user.password_hash):
            logger.warning(f"Invalid password for email: {request.email}")
            raise ValidationError(message="Invalid email or password")

        # 2️⃣ Create JWT (SAME payload as register)
        logger.info("Generating access token")
        access_token = create_access_token({
            "userId": user.user_id,
            "roleId": user.role_id,
            "organizationId": user.organization_id,
            "branchId": user.branch_id,
            "groupId": user.group_id,
            "subGroupId": user.sub_group_id
        })

        logger.info(f"Login successful for email: {request.email}")

        return {
            "success": True,
            "message": "Login successful",
            "accessToken": access_token,
            "tokenType": "Bearer",
            "user": {
                "id": user.user_id,
                "name": user.name,
                "email": user.email,
                "roleId": user.role_id,
                "organizationId": user.organization_id
            },
            "navigation": {
                "nextPage": "/dashboard"
            }
        }

    except ValidationError as ve:
        logger.error(f"Validation error during login: {str(ve)}")
        raise ve

    except Exception as unexpected_error:
        logger.error(f"Unexpected error during login: {str(unexpected_error)}")
        raise OnboardingError(
            message="An unexpected error occurred during login",
            details={"error": str(unexpected_error)}
        )
