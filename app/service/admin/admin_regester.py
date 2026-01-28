from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.admin.regester import AdminRegisterRequest
from app.models.user import User
from app.core.auth.security import hash_password, create_access_token
from sqlalchemy.future import select
from app.models.organization import Organization
from fastapi import Depends
from app.core.exceptions import EmailExistsError, ValidationError, DatabaseError, OnboardingError
import logging

# Configure logging
logger = logging.getLogger(__name__)

async def get_or_create_organization(
    db: AsyncSession,
    organization_name: str
):
    result = await db.execute(
        select(Organization)
        .where(Organization.name == organization_name)
    )
    org = result.scalars().first()

    if org:
        return org.organization_id  # 👈 reuse

    org = Organization(name=organization_name)
    db.add(org)
    await db.flush()   # 👈 commit se pehle ID mil jati hai

    return org.organization_id


async def register_admin(request: AdminRegisterRequest, db: AsyncSession=Depends(get_db)):
    """
    Register a new admin user
    
    Args:
        request: Admin registration request
        db: Database session
    
    Returns:
        Registration response with access token
    
    Raises:
        EmailExistsError: If email already registered
        ValidationError: If password validation fails
        DatabaseError: If database operations fail
        OnboardingError: If registration fails
    """
    try:
        logger.info(f"Starting admin registration for email: {request.email}")
        
        async with db.begin():  # 🔐 transaction start

            # 1. Email check
            logger.info(f"Checking if email already exists: {request.email}")
            result = await db.execute(
                select(User).where(User.email == request.email)
            )
            if result.scalar_one_or_none():
                logger.warning(f"Email already registered: {request.email}")
                raise EmailExistsError(request.email)

            # 2. Password hash and validation
            logger.info("Validating password and confirm password")
            if request.password != request.confirm_password:
                logger.warning(f"Password mismatch for email: {request.email}")
                raise ValidationError(
                    message="Password and confirm password do not match"
                )
            
            hashed_password = hash_password(request.password)
            logger.info("Password hashed successfully")

            # 3. Get or create organization
            logger.info(f"Setting up organization: {request.organization_name}")
            organization_id = await get_or_create_organization(
                db, request.organization_name
            )
            logger.info(f"Organization setup complete with ID: {organization_id}")

            # 4. Create admin user
            logger.info(f"Creating admin user: {request.name}")
            new_user = User(
                name=request.name,
                email=request.email,
                phone=request.phone,
                password_hash=hashed_password,

                role_id=1,  # SUPER_ADMIN
                organization_id=organization_id,

                branch_id=None,
                group_id=None,
                sub_group_id=None,

                status="ACTIVE"
            )

            db.add(new_user)
            await db.flush()  # user_id mil jata hai
            logger.info(f"Admin user created with ID: {new_user.user_id}")

        # 🔓 transaction auto-commit here
        logger.info("Transaction committed successfully")

        # 5. JWT
        logger.info("Generating access token")
        access_token = create_access_token({
            "userId": new_user.user_id,
            "roleId": new_user.role_id,
            "organizationId": new_user.organization_id,
            "branchId": None,
            "groupId": None,
            "subGroupId": None
        })

        logger.info(f"Admin registration completed successfully for: {request.email}")
        return {
            "success": True,
            "message": "Admin registered successfully",
            "accessToken": access_token,
            "tokenType": "Bearer",
            "user": {
                "id": new_user.user_id,
                "name": new_user.name,
                "email": new_user.email,
                "role": "SUPER_ADMIN"
            }
        }
    
    except (EmailExistsError, ValidationError, DatabaseError) as app_error:
        logger.error(f"Application error during admin registration: {str(app_error)}")
        raise app_error
    
    except Exception as unexpected_error:
        logger.error(f"Unexpected error during admin registration: {str(unexpected_error)}")
        raise OnboardingError(
            message="An unexpected error occurred during admin registration",
            details={"error": str(unexpected_error)}
        )
    
