from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.admin.regester import AdminRegisterRequest
from app.models.user import User
from app.core.auth.security import hash_password, create_access_token
from sqlalchemy.future import select
from app.models.organization import Organization
from fastapi import Depends, HTTPException

async def get_or_create_organization(
    db: AsyncSession,
    organization_name: str
):
    result = await db.execute(
        select(Organization)
        .where(Organization.name == organization_name)
    )
    org = result.scalar_one_or_none()

    if org:
        return org.organization_id  # 👈 reuse

    org = Organization(name=organization_name)
    db.add(org)
    await db.flush()   # 👈 commit se pehle ID mil jati hai

    return org.organization_id


async def register_admin(request: AdminRegisterRequest, db: AsyncSession=Depends(get_db)):

    async with db.begin():  # 🔐 transaction start

        # 1. Email check
        result = await db.execute(
            select(User).where(User.email == request.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # 2. Password hash
        hashed_password = hash_password(request.password)

        # 3. Get or create organization
        organization_id = await get_or_create_organization(
            db, request.organization_name
        )

        # 4. Create admin user
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

    # 🔓 transaction auto-commit here

    # 5. JWT
    access_token = create_access_token({
        "userId": new_user.user_id,
        "roleId": new_user.role_id,
        "organizationId": new_user.organization_id,
        "branchId": None,
        "groupId": None,
        "subGroupId": None
    })

    return {
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
    
