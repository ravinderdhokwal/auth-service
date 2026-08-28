from contextlib import asynccontextmanager
import logging
from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.core import settings
from auth_service.db.session import async_engine, get_db_session


logger = logging.getLogger(settings.APPLICATION_NAME)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APPLICATION_NAME, lifespan=lifespan)

    # app.include_router()

    @app.get("/health", tags=["health check", "db health"])
    async def check_health(db: AsyncSession = Depends(get_db_session)):
        try:
            await db.execute(text("SELECT 1"))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"database": "connected"}
            )
        except Exception as exc:
            logger.error("DATABASE HEALTH CHECK FAILED: ", exc_info=exc)
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"database": "unreachable"}
            )

    return app

app = create_app()