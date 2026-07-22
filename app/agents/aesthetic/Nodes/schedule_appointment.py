import uuid
from langgraph.types import Command

from app.db.connection import get_supabase
from app.config.credentials_config import config
from app.agents.aesthetic.state.aesthic_state import AestheticState


async def ScheduleAppointment(state: AestheticState):
    try:
        supabase = get_supabase()

        appointment = {
        "appointment_id": str(uuid.uuid4()),
        "company_name": state["company_name"],
        "patient_name": state["message"],
        "phone_number": state["phone_number"],
        "treatment": state["treatment"],
        "appointment_date": state["appointment_date"],
        "appointment_time": state["appointment_time"],
        "appointment_status": "scheduled",
    }

        result = (
            supabase.table(config.SUPABASE_TABLE_APPOINTMENT)
            .insert(appointment)
            .execute()
        )

        return Command(
            update={
                "appointment": result.data[0] if result.data else None,
                "appointment_status": "scheduled",
            },
            goto="next_node",  # Replace with your next node
        )

    except Exception as e:
        print(f"Error scheduling appointment: {e}")

        return Command(
            update={
                "appointment_status": "failed",
                "error": str(e),
            },
            goto="error_handler",  # Replace with your error node
        )