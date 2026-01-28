from fastapi import FastAPI
from app.api.api_collection import api_router
from app.core.database import engine ,Base
import app.models  # ensure all models are imported so metadata is registered


app = FastAPI(title="Async FastAPI with PostgreSQL")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # create_all requires all model modules to be imported so tables are registered
        await conn.run_sync(Base.metadata.create_all)


app.include_router(api_router, prefix="/api")
