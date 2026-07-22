

from app.agents.aesthetic.state.aesthic_state import AestheticState


async def human_handoff(state: AestheticState) -> AestheticState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    return Command(
        update={"appointment": "human handoff required"},
        goto="human_handoff"
    )