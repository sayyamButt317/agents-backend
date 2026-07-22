from typing import cast

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.types import Command

from app.agents.aesthetic.state.aesthic_state import (
    AestheticState,
    IntentClassification,
)

INTENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an intent classification assistant for an aesthetic clinic.

Your ONLY responsibility is to classify the user's primary intent.

Intent definitions:

- booking:
  User wants to book a NEW treatment appointment.

- consultation:
  User wants to schedule a consultation.

- request_appointment:
  User is asking about an EXISTING appointment.

- reschedule:
  User wants to change an EXISTING appointment.

- cancellation:
  User wants to cancel an EXISTING appointment.

- pricing:
  User asks about prices, discounts or packages.

- treatment:
  User asks about Botox, fillers, laser,
  HydraFacial, PRP, recovery, side effects, etc.

- info:
  User asks about clinic information.

- faq:
  Frequently asked questions.

- review:
  Positive feedback.

- complaint:
  Complaint.

- suggestion:
  Suggestion.

- other:
  Anything else.

Return ONLY the structured response.
"""
        ),
        ("human", "{message}"),
    ]
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

INTENT_CLASSIFIER = (
    INTENT_PROMPT
    | llm.with_structured_output(IntentClassification)
)

CONFIDENCE_THRESHOLD = 0.60


async def IntentClassifier(
    state: AestheticState,
) -> Command:
    print(f"Entering into Intent Classifier: {state['message']}")
    classification = cast(
        IntentClassification,
        await INTENT_CLASSIFIER.ainvoke(
            {
                "message": state["message"],
            }
        ),
    )

    if classification.confidence < CONFIDENCE_THRESHOLD:
        return Command(
            update={
                "classification": classification,
                "response": (
                    "I'm not completely sure I understood your request. "
                    "Could you please rephrase it?"
                ),
            },
            goto="generate_response",
        )

    return Command(
        update={
            "classification": classification,
        },
        goto="appointment_details_extractor",
    )