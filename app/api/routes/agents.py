from fastapi import APIRouter
from app.agents.aesthetic.invoke.aesthetic_invoke import AestheticInvoke
from app.agents.aesthetic.state.aesthic_state import AestheticRequest, AestheticState



router = APIRouter()


@router.post("/aesthetic-agent")
async def aesthetic_agent(request: AestheticRequest):
    return await AestheticInvoke(AestheticState(**request.model_dump()))