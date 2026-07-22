import uuid

from langgraph.types import Command

from app.config.credentials_config import config
from app.db.connection import get_supabase
from app.agents.aesthetic.state.aesthic_state import AestheticState


async def ScheduleAppointment(state: AestheticState) -> Command:
    try:
        print("Entering into Scheduling appointment...")
        required_fields = {
            "company_name": state.get("company_name"),
            "patient_name": state.get("patient_name"),
            "phone_number": state.get("phone_number"),
            "treatment": state.get("treatment"),
            "new_appointment_date": state.get("new_appointment_date"),
            "new_appointment_time": state.get("new_appointment_time"),
        }

        missing = [k for k, v in required_fields.items() if not v]

        if missing:
            return Command(
                update={
                    "response": (
                        "I'm missing the following information to schedule your appointment: "
                        + ", ".join(missing)
                    )
                },
                goto="generate_response",
            )

        supabase = get_supabase()

        appointment = {
            "appointment_id": str(uuid.uuid4()),
            "company_name": state["company_name"],
            "patient_name": state["patient_name"],
            "phone_number": state["phone_number"],
            "treatment": state["treatment"],
            "appointment_date": state["new_appointment_date"],
            "appointment_time": state["new_appointment_time"],
            "appointment_status": "scheduled",
        }

        result = (
            supabase.table(config.SUPABASE_TABLE_APPOINTMENT)
            .insert(appointment)
            .execute()
        )

        appointment_data = result.data[0] if result.data else None

        return Command(
            update={
                "appointment": appointment_data,
                "appointment_status": "scheduled",
                "response": (
                    f"Your {appointment['treatment']} appointment has been "
                    f"scheduled for {appointment['appointment_date']} at "
                    f"{appointment['appointment_time']}."
                ),
            },
            goto="generate_response",
        )

    except Exception as e:
        print(f"Schedule appointment error: {e}")

        return Command(
            update={
                "appointment": None,
                "appointment_status": "failed",
                "error": str(e),
                "response": (
                    "Sorry, I couldn't schedule your appointment at the moment. "
                    "Please try again later."
                ),
            },
            goto="generate_response",
        )