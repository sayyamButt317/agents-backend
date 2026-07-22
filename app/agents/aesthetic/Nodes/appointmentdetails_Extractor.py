from typing import cast

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.types import Command

from app.agents.aesthetic.state.aesthic_state import (
    AestheticState,
    AppointmentDetails,
)

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an appointment information extractor for an aesthetic clinic.

Current intent:
{intent}

Extract ONLY the information explicitly mentioned by the user.

Rules:
- Never guess missing values.
- Return null for fields that are not mentioned.
- Convert dates to YYYY-MM-DD format whenever possible.
- Convert times to HH:MM (24-hour) whenever possible.

Intent-specific rules:

BOOKING:
- Populate ONLY:
    - patient_name
    - phone_number
    - treatment
    - new_appointment_date
    - new_appointment_time

REQUEST_APPOINTMENT:
- Populate:
    - current_appointment_date
    - current_appointment_time

CANCELLATION:
- Populate:
    - current_appointment_date
    - current_appointment_time

RESCHEDULE:
- Populate:
    - current_appointment_date
    - current_appointment_time
    - new_appointment_date
    - new_appointment_time

Never invent dates or times.
If a value is missing, return null.
"""
        ),
        ("human", "{message}"),
    ]
)

extractor = (
    PROMPT
    | ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    ).with_structured_output(AppointmentDetails)
)


async def AppointmentDetailsExtractor(
    state: AestheticState,
) -> Command:

    details = cast(
        AppointmentDetails,
        await extractor.ainvoke(
            {
                "message": state["message"],
                "intent": state["classification"].intent.value,
            }
        ),
    )

    return Command(
        update={
            "patient_name": details.patient_name
            or state.get("patient_name"),

            "phone_number": details.phone_number
            or state.get("phone_number"),

            "treatment": details.treatment
            or state.get("treatment"),

            "current_appointment_date": (
                details.current_appointment_date
                or state.get("current_appointment_date")
            ),

            "current_appointment_time": (
                details.current_appointment_time
                or state.get("current_appointment_time")
            ),

            "new_appointment_date": (
                details.new_appointment_date
                or state.get("new_appointment_date")
            ),

            "new_appointment_time": (
                details.new_appointment_time
                or state.get("new_appointment_time")
            ),
        },
        goto="collect_appointment_details",
    )