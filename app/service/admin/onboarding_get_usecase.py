from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.usecase import InfoUseCase
from app.models.user import User

async def fetch_info_usecases(
    db: AsyncSession,
    current_user: User
):
    result = await db.execute(
        select(InfoUseCase)
        .where(InfoUseCase.is_active == True)
        .order_by(InfoUseCase.use_case_name)
    )

    usecases = result.scalars().all()

    return {
        "success": True,
        "usecases": [
            {
                "use_case_id": uc.use_case_id,
                "use_case_name": uc.use_case_name,
                "description": uc.description
            }
            for uc in usecases
        ]
    }
