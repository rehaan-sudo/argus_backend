from fastapi import FastAPI
from app.api.api_collection import api_router
from app.core.database import engine, Base

app = FastAPI(title="Async FastAPI with PostgreSQL")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router, prefix="/api")
