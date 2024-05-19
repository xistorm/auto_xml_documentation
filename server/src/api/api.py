from fastapi import APIRouter

from src.api.endpoints import documentation, ping

api_router = APIRouter()
api_router.include_router(ping.router, prefix='/ping')
api_router.include_router(documentation.router, prefix='/documentation')
