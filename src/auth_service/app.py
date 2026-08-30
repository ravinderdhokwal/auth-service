from contextlib import asynccontextmanager
import logging
from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.core import settings
from auth_service.core.exceptions import AppException
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
    
    @app.exception_handler(AppException)
    async def app_exception_handler(req: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "error": type(exc).__name__,
                "data": exc.data if exc.data else None
            }
        )
    
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("UNHANDLED EXCEPTION : ", exc_info=str(exc), extra={"path": request.url.path})
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(exc) if settings.IS_DEV_ENV else "Internal Server Error"
            }
        )

    return app

app = create_app()