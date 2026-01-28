from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from ...service.admin.admin_regester import register_admin 
from app.schemas.admin.regester import AdminRegisterRequest

router = APIRouter()

@router.post("/register/admin")
async def register_admin_api(
    request: AdminRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    return await register_admin(request, db)

