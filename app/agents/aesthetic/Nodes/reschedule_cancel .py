from app.agents.aesthetic.state.aesthic_state import AestheticState
from typing import Literal
from langgraph.types import Command
from langchain_openai import ChatOpenAI


async def reschedule_cancel_appointment(state: AestheticState) -> AestheticState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    return Command(
        update={"appointment": "cancelled successfully"},
        goto="reschedule_cancel_appointment"
    )