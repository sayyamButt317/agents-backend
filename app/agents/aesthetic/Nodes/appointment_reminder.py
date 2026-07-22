
from langgraph.types import Command
from app.agents.aesthetic.state.aesthic_state import AestheticState


async def AppointmentReminder(state: AestheticState) -> Command:
    return Command(
        update={"response": "appointment reminder sent successfully"},
        goto="end"
    )
