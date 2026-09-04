from fastapi import APIRouter

from auth_service.api.endpoints import auth_api


api_router = APIRouter()

api_router.include_router(auth_api.router)