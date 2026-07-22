from typing_extensions import Final, Literal

from langgraph.types import Command

from app.agents.aesthetic.state.aesthic_state import (
    AestheticState,
    Intent,
)

NextNode = Literal[
    "schedule_appointment",
    "check_appointment",
    "reschedule_appointment",
    "search_documentation",
    "cancel_appointment",
    "feedback",
    "generate_response",
]

ROUTES: Final[dict[Intent, NextNode]] = {
    Intent.BOOKING: "schedule_appointment",
    Intent.CONSULTATION: "schedule_appointment",
    Intent.APPOINTMENT: "check_appointment",
    Intent.RESCHEDULE: "reschedule_appointment",
    Intent.CANCELLATION: "cancel_appointment",
    Intent.PRICING: "search_documentation",
    Intent.INFO: "search_documentation",
    Intent.FAQ: "search_documentation",
    Intent.TREATMENT: "search_documentation",
    Intent.REVIEW: "feedback",
    Intent.COMPLAINT: "feedback",
    Intent.SUGGESTION: "feedback",
    Intent.OTHER: "generate_response",
}


async def CollectAppointmentDetails(
    state: AestheticState,
) -> Command:
    print("Entering into Collecting appointment details...")
    intent = state["classification"].intent
    missing_fields: list[str] = []

    if intent in (Intent.BOOKING, Intent.CONSULTATION):
        if not state.get("patient_name"):
            missing_fields.append("patient name")
        if not state.get("phone_number"):
            missing_fields.append("phone number")
        if not state.get("treatment"):
            missing_fields.append("treatment")
        if not state.get("new_appointment_date"):
            missing_fields.append("appointment date")
        if not state.get("new_appointment_time"):
            missing_fields.append("appointment time")
    elif intent == Intent.CANCELLATION:
        if not state.get("phone_number"):
            missing_fields.append("phone number")

        if not state.get("current_appointment_date"):
            missing_fields.append("appointment date")

        if not state.get("current_appointment_time"):
            missing_fields.append("appointment time")

    elif intent == Intent.RESCHEDULE:

        if not state.get("phone_number"):
            missing_fields.append("phone number")

        if not state.get("current_appointment_date"):
            missing_fields.append("current appointment date")

        if not state.get("current_appointment_time"):
            missing_fields.append("current appointment time")

        if not state.get("new_appointment_date"):
            missing_fields.append("new appointment date")

        if not state.get("new_appointment_time"):
            missing_fields.append("new appointment time")

    elif intent == Intent.APPOINTMENT:

        if not state.get("phone_number"):
            missing_fields.append("phone number")

    if missing_fields:
        return Command(
            update={
                "response": (
                    "I just need your "
                    + ", ".join(missing_fields)
                    + " to continue."
                )
            },
            goto="generate_response",
        )

    return Command(
        update={},
        goto=ROUTES[intent],
    )