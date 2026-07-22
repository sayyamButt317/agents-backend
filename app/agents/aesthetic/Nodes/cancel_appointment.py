from typing import cast

from langgraph.types import Command

from app.config.credentials_config import config
from app.db.connection import get_supabase
from app.agents.aesthetic.state.aesthic_state import (
    AestheticState,
    AppointmentState,
)


async def CancelAppointment(state: AestheticState) -> Command:
    try:
        print("Entering into Cancelling appointment...")
        # Validate required fields
        required_fields = {
            "company_name": state.get("company_name"),
            "phone_number": state.get("phone_number"),
            "current_appointment_date": state.get("current_appointment_date"),
            "current_appointment_time": state.get("current_appointment_time"),
        }

        missing = [
            key for key, value in required_fields.items() if not value
        ]

        if missing:
            return Command(
                update={
                    "response": (
                        "I'm missing the following information to cancel your appointment: "
                        + ", ".join(missing)
                    )
                },
                goto="generate_response",
            )

        supabase = get_supabase()

        result = (
            supabase.table(config.SUPABASE_TABLE_APPOINTMENT)
            .update(
                {
                    "appointment_status": "cancelled",
                }
            )
            .eq("company_name", state["company_name"])
            .eq("phone_number", state["phone_number"])
            .eq(
                "appointment_date",
                state["current_appointment_date"],
            )
            .eq(
                "appointment_time",
                state["current_appointment_time"],
            )
            .neq("appointment_status", "cancelled")
            .execute()
        )

        appointments = cast(
            list[AppointmentState],
            result.data or [],
        )

        if not appointments:
            return Command(
                update={
                    "appointment": None,
                    "appointment_status": None,
                    "response": (
                        "I couldn't find an active appointment matching the details you provided."
                    ),
                },
                goto="generate_response",
            )

        cancelled_appointment = appointments[0]

        appointment_date = cancelled_appointment["appointment_date"]
        appointment_time = cancelled_appointment["appointment_time"]

        return Command(
            update={
                "appointment": cancelled_appointment,
                "appointment_status": "cancelled",
                "response": (
                    f"Your appointment on {appointment_date} "
                    f"at {appointment_time} has been cancelled successfully. "
                    "If you'd like to book another appointment, I'm happy to help."
                ),
            },
            goto="generate_response",
        )

    except Exception as e:
        print(f"Cancel appointment error: {e}")

        return Command(
            update={
                "appointment": None,
                "appointment_status": None,
                "error": str(e),
                "response": (
                    "Sorry, I couldn't cancel your appointment at the moment. "
                    "Please try again later."
                ),
            },
            goto="generate_response",
        )