import random
import hashlib
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.core.database import get_db
from app.models.email_otp import EmailOTP
from app.schemas.email_otp import SendOTPRequest, VerifyOTPRequest
from app.service.email_service import send_email_otp

router = APIRouter(prefix="/auth", tags=["Email Verification"])


def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()

@router.post("/send-otp")
async def send_otp(
    request: SendOTPRequest,
    db: AsyncSession = Depends(get_db)
):
    otp = str(random.randint(100000, 999999))
    otp_hash = hash_otp(otp)

    await db.execute(
        delete(EmailOTP).where(EmailOTP.email == request.email)
    )

    record = EmailOTP(
        email=request.email,
        otp_hash=otp_hash,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(record)
    await db.commit()

    send_email_otp(request.email, otp)

    return {
        "success": True,
        "message": "OTP sent successfully"
    }


@router.post("/verify-otp")
async def verify_otp(request: VerifyOTPRequest,     db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EmailOTP).where(EmailOTP.email == request.email)
    )
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(400, "OTP not found")

    if record.expires_at < datetime.utcnow():
        raise HTTPException(400, "OTP expired")

    if record.otp_hash != hash_otp(request.otp):
        raise HTTPException(400, "Invalid OTP")

    # ✅ OTP verified → DELETE
    await db.delete(record)
    await db.commit()

    return {
        "success": True,
        "message": "Email verified successfully"
    }
