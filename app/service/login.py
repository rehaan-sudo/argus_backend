from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate

async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_users(db: AsyncSession):
    result = await db.execute(select(User).where(User.is_active == True))
    return result.scalars().all()



async def get_user_by_email(db: AsyncSession, email: str):
    result= await db.execute(select(User).where(User.email == email))
    return result.scalars().first()