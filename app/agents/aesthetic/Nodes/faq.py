from app.agents.aesthetic.state.aesthic_state import AestheticState
from langgraph.types import Command


async def FAQ(state: AestheticState) -> Command:
    return Command(
        update={"response": "FAQ"},
        goto="faq"
    )