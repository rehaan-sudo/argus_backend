from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.admin.regester import AdminRegisterRequest
from app.models.user import User
from app.core.security import hash_password, create_access_token
from sqlalchemy.future import select
from app.models.organization import Organization
from fastapi import HTTPException


async def register_admin(request: AdminRegisterRequest, db: AsyncSession):

    # 1. Check email already exists
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash password
    hashed_password = hash_password(request.password)

    # 3. Create admin user
    new_user = User(
        name=request.name,
        email=request.email,
        phone=request.phone,
        password_hash=hashed_password,

        role_id=1,  # ADMIN
        organization_id=request.organization_id,
        branch_id=None

        group_id=None,
        sub_group_id=None,

        status="ACTIVE"
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # 4. Generate JWT
    token = create_access_token({
        "user_id": new_user.user_id,
        "role": "ADMIN",
        "branch_id": new_user.branch_id
    })

    return {
        "message": "Admin registered successfully",
        "access_token": token,
        "token_type": "Bearer",
        "user": {
            "id": new_user.user_id,
            "name": new_user.name,
            "email": new_user.email,
            "role": "ADMIN"
        }
    }
async def organization_store_name(db: AsyncSession, request: AdminRegisterRequest):
  org = Organization(
        name=request.name
    )

    db.add(org)
    await db.commit()
    await db.refresh(org)
  return 