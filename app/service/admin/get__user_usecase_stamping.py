from app.core.database import get_db
from app.core.exceptions import AppException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends, status


async def get_user_usecase_stampings(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        query = text("""
            SELECT
                iuc.use_case_id,
                iuc.use_case_name,
                s.stamping_id,
                s.stamping_name
            FROM user_usecase uu
            JOIN info_use_cases iuc
                ON uu.usecase_name = iuc.use_case_name
            JOIN info_usecase_stamping s
                ON iuc.use_case_id = s.use_case_id
            WHERE uu.user_id = :user_id
              AND iuc.is_active = true;
        """)

        result = await db.execute(query, {"user_id": user_id})
        rows = result.fetchall()

        if not rows:
            raise AppException(
                message="No usecases or stampings found for this user",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="DATA_NOT_FOUND"
            )

        response = {}

        for row in rows:
            uc_id = row.use_case_id

            if uc_id not in response:
                response[uc_id] = {
                    "use_case_id": uc_id,
                    "use_case_name": row.use_case_name,
                    "stampings": []
                }

            response[uc_id]["stampings"].append({
                "stamping_id": row.stamping_id,
                "stamping_name": row.stamping_name
            })

        return {
            "success": True,
            "message": "Stampings fetched successfully",
            "user_id": user_id,
            "data": list(response.values())
        }

    except AppException:
        raise

    except SQLAlchemyError:
        raise AppException(
            message="Database error while fetching stampings",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR"
        )

    except Exception:
        raise AppException(
            message="Unexpected server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_SERVER_ERROR"
        )
