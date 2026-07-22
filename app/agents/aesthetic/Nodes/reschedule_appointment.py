from langgraph.types import Command

from app.config.credentials_config import config
from app.db.connection import get_supabase
from app.agents.aesthetic.state.aesthic_state import AestheticState


async def RescheduleAppointment(state: AestheticState):
    try:
        print("Entering into Rescheduling appointment...")
        supabase = get_supabase()
        update_data = {
            "appointment_date": state["new_appointment_date"],
            "appointment_time": state["new_appointment_time"],
            "treatment": state["treatment"],
            "appointment_status": "rescheduled",
        }

        result = (
            supabase.table(config.SUPABASE_TABLE_APPOINTMENT)
            .update(update_data)
            .eq("company_name", state["company_name"])
            .eq("phone_number", state["phone_number"])
            .eq("appointment_date", state["current_appointment_date"])
            .eq("appointment_time", state["current_appointment_time"])
            .neq("appointment_status", "cancelled")
            .execute()
        )

        appointments = result.data or []

        if not appointments:
            return Command(
                update={
                    "appointment": None,
                    "response": "I couldn't find your appointment to reschedule.",
                },
                goto="generate_response",
            )

        return Command(
            update={
                "appointment": appointments[0],
                "appointment_status": "rescheduled",
                "response": (
                    "Your appointment has been successfully rescheduled."
                ),
            },
            goto="generate_response",
        )

    except Exception as e:
        print(f"Reschedule appointment error: {e}")

        return Command(
            update={
                "appointment": None,
                "error": str(e),
                "response": (
                    "Sorry, I couldn't reschedule your appointment right now."
                ),
            },
            goto="generate_response",
        )