from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.admin.onboarding import CameraOnboardingRequest
from app.models.user import User
from app.models.organization import Organization
from app.models.branch import Branch
from app.models.user_usecase import UserUseCase
from app.models.vpn_config import VpnConfig
from app.models.camera import Camera
from app.core.auth.security import hash_password, create_access_token
from app.core.auth.dependency import get_current_user

async def complete_onboarding(
    request: CameraOnboardingRequest,
    db: AsyncSession,
    current_user: User
):
    async with db.begin():

        # Organization
        org = Organization(name=request.company_name)
        db.add(org)
        await db.flush()

        # Branch
        branch = Branch(
            organization_id=org.organization_id,
            branch_name=request.branch_name
        )
        db.add(branch)
        await db.flush()

        # Use cases
        for uc in request.use_cases_list:
            db.add(UserUseCase(
                branch_id=branch.branch_id,
                usecase=uc,
                details="enabled"
            ))

        # VPN
        vpn = VpnConfig(
            branch_id=branch.branch_id,
            username=request.vpn_user_name,
            password=hash_password(request.vpn_password),
            site=request.site_name,
            config_file_path=request.file_upload
        )
        db.add(vpn)
        await db.flush()

        # Camera
        camera = Camera(
            vpn_confige=vpn.vpn_id,
            camera_name=request.camera_name,
            camera_type="RTSP",
            IP=request.ip_address,
            cam_zone=request.camera_zone,
            port=request.port
        )
        db.add(camera)

    # 🔥 EXTENDED JWT
    token_payload = {
        "userId": current_user.user_id,
        "roleId": current_user.role_id,
        "organizationId": org.organization_id,
        "branchId": branch.branch_id,
        "useCases": request.use_cases_list,
        "vpnEnabled": True,
        "onboardingCompleted": True
    }

    access_token = create_access_token(token_payload)

    return {
        "success": True,
        "access_token": access_token,
        "nextPage": "/dashboard"
    }
