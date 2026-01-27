from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from service.admin.admin_regester import register_admin
router = APIRouter()

@router.post("/register/admin")
async def register_admin(request: AdminRegisterRequest, db: AsyncSession):
    return await register_admin(request, db)
    
