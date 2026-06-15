from fastapi import APIRouter
from app.api.routes.agent_routes import agent_router

api_router = APIRouter()
api_router.include_router(agent_router, prefix="/api/agent", tags=["Agent"])
