from fastapi import APIRouter
from app.api.routes.ws_route import router as ws_router

api_router = APIRouter()
api_router.include_router(ws_router, prefix="/api/ws", tags=["WS"])
