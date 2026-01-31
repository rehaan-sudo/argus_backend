from fastapi import FastAPI
from app.api.api_collection import api_router
from app.core.database import engine, Base
from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    general_exception_handler,
    value_error_handler,
    runtime_error_handler
)
import app.models  # ensure all models are imported so metadata is registered
from app.core.utils import logger
from app.api.router.email_verification import router as email_router

from app.core.add_cors_middleware import add_cors_middleware

app = FastAPI(title="Async FastAPI with PostgreSQL")
logger.info("Starting FastAPI application.")

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(RuntimeError, runtime_error_handler)
app.add_exception_handler(Exception, general_exception_handler)




@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # create_all requires all model modules to be imported so tables are registered
        await conn.run_sync(Base.metadata.create_all)


add_cors_middleware(app)
app.include_router(api_router, prefix="/api")


app.include_router(email_router)
