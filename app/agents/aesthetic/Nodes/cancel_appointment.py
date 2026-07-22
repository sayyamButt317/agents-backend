from langgraph.types import Command
from app.agents.aesthetic.state.aesthic_state import AestheticState


async def CancelAppointment(state: AestheticState) -> Command:
    return Command(
        update={"response": "Appointment canceled successfully"},
        goto="cancel_appointment"
    )
