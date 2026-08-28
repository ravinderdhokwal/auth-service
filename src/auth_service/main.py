import uvicorn

from auth_service.core import settings

def main():
    uvicorn.run(
        "auth_service.app:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )