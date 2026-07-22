from langgraph.types import Command

from app.config.credentials_config import config
from app.db.connection import get_supabase
from app.agents.aesthetic.state.aesthic_state import AestheticState


async def CheckAppointment(state: AestheticState):
    try:
        print("Entering into Checking appointment...")
        supabase = get_supabase()
        result = (
            supabase.table(config.SUPABASE_TABLE_APPOINTMENT)
            .select("*")
            .eq("companyname", state.get("company_name"))
            .eq("appointment_date", state.get("appointment_date"))
            .eq("appointment_time", state.get("appointment_time"))
            .neq("status", "cancelled")
            .execute()
        )

        appointments = result.data or []

        if appointments:
            return Command(
                update={
                    "appointment": appointments[0],
                    "response": (
                        "Sorry, that appointment slot is already booked. "
                        "Please choose another date or time."
                    ),
                },
                goto="generate_response",
            )

        return Command(
            update={
                "appointment": None,
            },
            goto="schedule_appointment",
        )

    except Exception as e:
        print(f"Error checking appointment: {e}")

        return Command(
            update={
                "error": str(e),
                "response": (
                    "Sorry, I couldn't check appointment availability right now."
                ),
            },
            goto="generate_response",
        )