from fastapi import APIRouter

from src.api.endpoints import documentation

api_router = APIRouter()
api_router.include_router(documentation.router, prefix='/documentation')
