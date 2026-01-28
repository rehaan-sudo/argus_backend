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
from app.core.exceptions import CameraError, OnboardingError, DatabaseError
import logging

import cv2
import socket
import requests

# Configure logging
logger = logging.getLogger(__name__)

def check_camera(ip: str, port: int, path: str, timeout: int = 5) -> dict:
    """
    Check camera connectivity and health
    
    Args:
        ip: Camera IP address
        port: Camera port
        path: Camera stream path
        timeout: Connection timeout in seconds
    
    Returns:
        Dictionary with camera status information
    """
    result = {
        "ip": ip,
        "port": port,
        "path": path,
        "ip_status": False,
        "camera_status": False,
        "frame": None,
        "message": ""
    }

    # 1. IP + Port check (socket level)
    try:
        sock = socket.create_connection((ip, port), timeout=timeout)
        sock.close()
        result["ip_status"] = True
    except socket.timeout:
        logger.warning(f"Camera connection timeout: {ip}:{port}")
        result["message"] = f"Camera connection timeout after {timeout}s"
        return result
    except socket.error as e:
        logger.warning(f"IP/Port not reachable: {ip}:{port} - {str(e)}")
        result["message"] = f"IP/Port not reachable: {str(e)}"
        return result
    except Exception as e:
        logger.error(f"Unexpected error checking IP/Port: {str(e)}")
        result["message"] = f"Unexpected error: {str(e)}"
        return result

    # 2. Camera URL build
    # Mostly cameras use RTSP
    # Example: rtsp://username:password@ip:port/path
    camera_url = f"rtsp://{ip}:{port}/{path}"

    try:
        # 3. Try to capture one frame
        cap = cv2.VideoCapture(camera_url)

        if not cap.isOpened():
            logger.warning(f"Camera stream not opening: {camera_url}")
            cap.release()
            result["message"] = "Camera connected but stream not opening"
            return result

        ret, frame = cap.read()
        cap.release()

        if ret:
            result["camera_status"] = True
            result["frame"] = frame
            result["message"] = "Camera is working and frame captured successfully"
            logger.info(f"Camera health check passed: {ip}:{port}")
        else:
            logger.warning(f"Frame not received from camera: {ip}:{port}")
            result["message"] = "Camera connected but frame not received"
    
    except Exception as e:
        logger.error(f"Error during camera frame capture: {str(e)}")
        result["message"] = f"Error capturing frame: {str(e)}"
    
    return result


async def complete_onboarding(
    request: CameraOnboardingRequest,
    db: AsyncSession,
    current_user: User
):
    """
    Complete admin onboarding process
    
    Args:
        request: Onboarding request with camera, VPN, and organization details
        db: Database session
        current_user: Current authenticated user
    
    Returns:
        Onboarding response with access token
    
    Raises:
        CameraError: If camera check fails
        OnboardingError: If onboarding process fails
        DatabaseError: If database operations fail
    """
    try:
        logger.info(f"Starting onboarding for user: {current_user.user_id}")
        
        # Camera validation
        logger.info(f"Validating camera: {request.ip_address}:{request.port}")
        camera_check_result = check_camera(
            ip=request.ip_address,
            port=request.port,
            path=""
        )
        
        if not camera_check_result["ip_status"]:
            logger.error(f"Camera IP/Port unreachable: {camera_check_result['message']}")
            raise CameraError(
                message="Camera IP/Port is not reachable",
                details={
                    "ip": request.ip_address,
                    "port": request.port,
                    "reason": camera_check_result["message"]
                }
            )
        
        if not camera_check_result["camera_status"]:
            logger.warning(f"Camera stream issue: {camera_check_result['message']}")
            # Continue with warning, as IP is reachable
        
        try:
            logger.info(f"Creating organization: {request.company_name}")
            # Organization
            org = Organization(name=request.company_name)
            db.add(org)
            await db.flush()
            logger.info(f"Organization created with ID: {org.organization_id}")

            # Branch
            logger.info(f"Creating branch: {request.branch_name}")
            branch = Branch(
                organization_id=org.organization_id,
                branch_name=request.branch_name
            )
            db.add(branch)
            await db.flush()
            logger.info(f"Branch created with ID: {branch.branch_id}")

            # Use cases
            logger.info(f"Adding use cases: {request.use_cases_list}")
            for uc in request.use_cases_list:
                db.add(UserUseCase(
                    branch_id=branch.branch_id,
                    usecase=uc,
                    details="enabled"
                ))
            

            # VPN Configuration
            logger.info("Configuring VPN settings")
            vpn = VpnConfig(
                branch_id=branch.branch_id,
                username=request.vpn_user_name,
                password=hash_password(request.vpn_password),
                site=request.site_name,
                config_file_path=request.file_upload,
                is_active=True
            )
            db.add(vpn)
            await db.flush()
            logger.info(f"VPN configured with ID: {vpn.vpn_id}")

            # Camera Registration
            logger.info("Registering camera")
            camera = Camera(
                vpn_confige=vpn.vpn_id,
                camera_name=request.camera_name,
                camera_type="RTSP",
                IP=request.ip_address,
                cam_zone=request.camera_zone,
                port=request.port,
                is_active=True
            )
            db.add(camera)
            await db.flush()
            logger.info("Camera registered")

            # Commit transaction
            await db.commit()
            logger.info("Onboarding transaction committed successfully")
        
        except Exception as db_error:
            await db.rollback()
            logger.error(f"Database error during onboarding: {str(db_error)}")
            raise DatabaseError(
                message="Failed to save onboarding data",
                details={
                    "operation": "onboarding_setup",
                    "error": str(db_error)
                }
            )
        
        # Generate JWT Token
        logger.info(f"Generating access token for user: {current_user.user_id}")
        token_payload = {
            "userId": current_user.user_id,
            "roleId": current_user.role_id,
            "organizationId": org.organization_id,
            "branchId": branch.branch_id,
            "groupId": current_user.group_id,
            "subGroupId": current_user.sub_group_id,
            "useCases": request.use_cases_list,
            "vpnEnabled": True,
            "onboardingCompleted": True
        }

        access_token = create_access_token(token_payload)
        
        logger.info(f"Onboarding completed successfully for user: {current_user.user_id}")
        return {
            "success": True,
            "message": "Admin onboarding completed successfully",
            "access_token": access_token,
            "tokenType": "Bearer",
            "user": {
                "id": current_user.user_id,
                "organizationId": org.organization_id,
                "branchId": branch.branch_id
            },
            "nextPage": "/dashboard"
        }
    
    except (CameraError, DatabaseError) as app_error:
        logger.error(f"Application error during onboarding: {str(app_error)}")
        raise app_error
    
    except Exception as unexpected_error:
        logger.error(f"Unexpected error during onboarding: {str(unexpected_error)}")
        raise OnboardingError(
            message="An unexpected error occurred during onboarding",
            details={"error": str(unexpected_error)}
        )