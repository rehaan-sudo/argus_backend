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
from sqlalchemy import select


from app.models.usecase import InfoUseCase


import requests

import socket
import cv2
import logging

logger = logging.getLogger("camera_health")
logger.setLevel(logging.INFO)

import base64

def frame_to_base64(frame):
    if frame is None:
        return None
    success, buffer = cv2.imencode(".jpg", frame)
    if not success:
        return None
    return base64.b64encode(buffer).decode("utf-8")


def check_camera(ip: str, port: int, username: str, password: str, path: str, timeout: int = 5) -> dict:
    logger.info(f"[check_camera] Start camera check | IP={ip}, Port={port}, Path={path}")

    result = {
        "status": "failed",
        "ip": ip,
        "port": port,
         "path" :path,
        "username": username,
        "ip_status": False,
        "camera_status": False,
        "frame": None,
        "error_type": None,
        "message": None
    }

    # 1️⃣ IP + Port Check
    try:
        logger.info(f"[SocketCheck] Trying to connect {ip}:{port}")
        sock = socket.create_connection((ip, port), timeout=timeout)
        sock.close()
        result["ip_status"] = True
        logger.info(f"[SocketCheck] IP & Port reachable {ip}:{port}")

    except socket.timeout:
        logger.error(f"[SocketCheck] Timeout {ip}:{port}")
        result.update({
            "error_type": "SOCKET_TIMEOUT",
            "message": f"Connection timeout after {timeout} seconds"
        })
        return result

    except socket.error as e:
        logger.error(f"[SocketCheck] Socket error {ip}:{port} | {e}")
        result.update({
            "error_type": "SOCKET_ERROR",
            "message": f"IP/Port not reachable: {str(e)}"
        })
        return result

    except Exception as e:
        logger.exception(f"[SocketCheck] Unexpected error {ip}:{port}")
        result.update({
            "error_type": "UNKNOWN_SOCKET_ERROR",
            "message": str(e)
        })
        return result

    # 2️⃣ Build Camera URL
    camera_url = f"rtsp://{username}:{password}@{ip}:{port}/{path}"

    logger.info(f"[RTSP] Camera URL created: {camera_url}")

    # 3️⃣ Capture Frame
    try:
        logger.info(f"[FrameCapture] Opening stream")
        cap = cv2.VideoCapture(camera_url)

        if not cap.isOpened():
            cap.release()
            logger.error(f"[FrameCapture] Stream not opening: {camera_url}")
            result.update({
                "error_type": "STREAM_OPEN_FAILED",
                "message": "Camera connected but stream not opening"
            })
            return result

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            logger.error(f"[FrameCapture] Frame not received from camera")
            raise CameraError(
                message="Camera stream opened but frame not received",
                details={"ip": ip, "port": port, "path": path}
            )
        frame_base64 = frame_to_base64(frame)
        # ✅ SUCCESS
        logger.info(f"[Success] Camera working fine | {ip}:{port}")
        result.update({
            "status": "success",
            "camera_status": True,
            "frame": frame_base64,
            "message": "Camera is working and frame captured successfully",
            "camera_url": camera_url
        })
        return result

    except CameraError as ce:
        logger.error(f"[CameraError] {ce.message} | {ce.details}")
        result.update({
            "error_type": "FRAME_CAPTURE_ERROR",
            "message": ce.message,
            "details": ce.details
        })
        return result

    except Exception as e:
        logger.exception(f"[OpenCV] Unexpected error during frame capture")
        result.update({
            "error_type": "OPENCV_ERROR",
            "message": f"Unexpected error during frame capture: {str(e)}"
        })
        return result



async def complete_onboarding(
    request: CameraOnboardingRequest,
    db: AsyncSession,
    current_user: User
):
    try:
        logger.info(f"Starting onboarding for user: {current_user.user_id}")

        logger.info(f"Validating camera: {request.ip_address}:{request.port}")

        camera_check_result = check_camera(
            ip=request.ip_address,
            username=request.user_name,
            port=request.port,
            password=request.camera_password,
            path=request.camera_name
        )

        if not camera_check_result["ip_status"]:
            raise CameraError(
                message="Camera IP/Port is not reachable",
                details=camera_check_result
            )

        if not camera_check_result["camera_status"]:
            raise CameraError(
                message="Camera reachable but no frames",
                details=camera_check_result
            )

       
        try:
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

            use_case_ids = request.use_cases_list   # ✅ FIX

            result = await db.execute(
                select(InfoUseCase.use_case_name)
                .where(
                    InfoUseCase.use_case_id.in_(use_case_ids),
                    InfoUseCase.is_active == True
                )
            )

            usecase_names = result.scalars().all()

            if not usecase_names:
                raise ValueError("No valid use cases found")

            user_usecases = [
                UserUseCase(
                    user_id=current_user.user_id,  
                    usecase_name=name
                )
                for name in usecase_names
            ]

            db.add_all(user_usecases)
            await db.flush()

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

            camera = Camera(
                vpn_confige_id=vpn.vpn_id,
                camera_name=request.camera_name,
                user_name=request.user_name,
                password=request.camera_password,
                camera_type="RTSP",
                ip=request.ip_address,
                cam_zone=request.camera_zone,
                port=request.port,
                is_active=True
            )
            db.add(camera)
            await db.flush()

            # COMMIT
            await db.commit()

        except Exception as db_error:
            await db.rollback()
            raise DatabaseError(
                message="Failed to save onboarding data",
                details={"error": str(db_error)}
            )

        token_payload = {
            "userId": current_user.user_id,
            "roleId": current_user.role_id,
            "organizationId": current_user.organization_id,
            "branchId": current_user.branch_id,
            "groupId": current_user.group_id,
            "subGroupId": current_user.sub_group_id,
            "useCases": usecase_names,
            "onboardingCompleted": True
        }

        access_token = create_access_token(token_payload)

        return {
            "success": True,
            "message": "Admin onboarding completed successfully",
            "access_token": access_token,
            "tokenType": "Bearer",
            "frame": camera_check_result["frame"],
            "camera_url": camera_check_result["camera_url"],
            "nextPage": "/dashboard"
        }

    except (CameraError, DatabaseError) as err:
        raise err

    except Exception as err:
        raise OnboardingError(
            message="Unexpected onboarding error",
            details={"error": str(err)}
        )


