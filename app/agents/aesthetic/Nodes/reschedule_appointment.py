import uuid
from langgraph.types import Command
from app.agents.aesthetic.state.aesthic_state import AestheticState
from app.db.connection import get_supabase
from app.config.credentials_config import config

async def RescheduleAppointment(state: AestheticState):
    try:
        supabase = get_supabase()
        update_data = {
            "appointment_date": state["appointment_date"],
            "appointment_time": state["appointment_time"],
            "treatment": state["treatment"],
            "appointment_status": "rescheduled",
            "appointment_id": str(uuid.uuid4()),
        }

        result = (
            supabase.table(config.SUPABASE_TABLE_APPOINTMENT)
            .update(update_data)
            .eq("appointment_id", state["appointment_id"])
            .execute()
        )

        if not result.data:
            return Command(
                update={
                    "response": "I couldn't find that appointment."
                },
                goto="generate_response",
            )

        return Command(
            update={
                "response": "Your appointment has been successfully rescheduled."
            },
            goto="generate_response",
        )

    except Exception as e:
        print(e)

        return Command(
            update={
                "response": "Sorry, I couldn't reschedule your appointment."
            },
            goto="generate_response",
        )