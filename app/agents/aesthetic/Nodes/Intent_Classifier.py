from typing_extensions import Final, Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.types import Command

from app.agents.aesthetic.state.aesthic_state import (
    AestheticState,
    Intent,
    IntentClassifier,
)

INTENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an intent classification assistant for an aesthetic clinic.
Your task is ONLY to classify the user's intent.
Return a structured response.
Intent definitions:
- booking:
  User wants to book a treatment.
- consultation:
  User wants to schedule or inquire about a consultation.
- request_appointment:
  User asks about an existing appointment.
- pricing:
  User asks about prices, packages, discounts or cost.
- treatment:
  User asks about Botox, fillers, laser, HydraFacial,
  PRP, skin care, procedures, recovery, side effects,
  eligibility or treatment recommendations.
- info:
  User asks about clinic hours, location, doctors,
  contact details or general clinic information.
- faq:
  General frequently asked questions.
- cancellation:
  User wants to cancel an appointment.
- review:
  User is leaving positive feedback.
- complaint:
  User is unhappy or reporting an issue.
- suggestion:
  User is giving suggestions.
- other:
  Anything that doesn't fit the above.
Return the single best intent with a confidence score between 0 and 1.
""",
        ),
        ("human", "{message}"),
    ]
)

INTENT_CLASSIFIER = (INTENT_PROMPT| ChatOpenAI(model="gpt-4o-mini",temperature=0,).with_structured_output(IntentClassifier))

NextNode = Literal[
    "schedule_appointment",
    "search_documentation",
    "cancel_appointment",
    "feedback",
    "other",
    ]

ROUTES: Final[dict[Intent, NextNode]] = {
    Intent.BOOKING: "schedule_appointment",
    Intent.CONSULTATION: "schedule_appointment",
    Intent.APPOINTMENT: "schedule_appointment",

    Intent.PRICING: "search_documentation",
    Intent.INFO: "search_documentation",
    Intent.FAQ: "search_documentation",
    Intent.TREATMENT: "search_documentation",

    Intent.CANCELLATION: "cancel_appointment",

    Intent.REVIEW: "feedback",
    Intent.COMPLAINT: "feedback",
    Intent.SUGGESTION: "feedback",

    Intent.OTHER: "other",
}

CONFIDENCE_THRESHOLD = 0.60


async def IntentClassifier(
    state: AestheticState,
) -> Command:
    classification = await INTENT_CLASSIFIER.ainvoke({"message": state["message"]})
    return Command(update={"intent": classification["intent"], "confidence": classification["confidence"]},goto=ROUTES.get(classification["intent"], "other"))