from datetime import datetime
from langgraph.types import Command
from app.agents.aesthetic.state.aesthic_state import AestheticState
from app.config.credentials_config import config
from app.db.connection import get_supabase



async def CheckAppointment(state: AestheticState) -> Command:
    try:
        supabase = get_supabase()
        today = datetime.now().date().isoformat()
        result = (
            supabase.table(config.SUPABASE_TABLE_APPOINTMENT)
            .select("*")
            .eq("appointment_date", today)
            .execute()
        )

        appointments = result.data or []
        if appointments:
            return Command(
                update={
                    "appointment": appointments,
                    "has_appointment": True,
                },
                goto="next_node",   # Replace with your next node
            )

        return Command(
            update={
                "appointment": [],
                "has_appointment": False,
            },
            goto="next_node",
        )

    except Exception as e:
        print(f"Error checking appointments: {e}")

        return Command(
            update={
                "appointment": [],
                "has_appointment": False,
                "error": str(e),
            },
            goto="error_handler",
        )