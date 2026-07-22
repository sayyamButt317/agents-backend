from langgraph.types import Command
from app.agents.aesthetic.state.aesthic_state import AestheticState


async def MessageType(state: AestheticState) -> Command:
    return Command(
        update={"response": "Message type detected successfully"},
        goto="end",
    )