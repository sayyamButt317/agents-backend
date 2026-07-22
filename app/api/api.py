from fastapi import APIRouter
from app.api.routes.meta import router as meta_router
from app.api.routes.admin import router as admin_router
api_router = APIRouter()

api_router.include_router(meta_router, prefix="/api/meta", tags=["Meta"])
api_router.include_router(admin_router, prefix="/api/admin", tags=["Admin"])