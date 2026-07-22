from enum import Enum
from typing import TypedDict

from pydantic import BaseModel, Field

class Intent(str, Enum):
    PRICING = "pricing"
    TREATMENT = "treatment"
    CONSULTATION = "consultation"
    BOOKING = "booking"
    CANCELLATION = "cancellation"
    INFO = "info"
    APPOINTMENT = "request_appointment"
    FAQ = "faq"
    REVIEW = "review"
    COMPLAINT = "complaint"
    SUGGESTION = "suggestion"
    OTHER = "other"

class MessageType(str, Enum):
    AUDIO = "audio"
    TEXT = "text"
    VIDEO = "video"
    IMAGE = "image"
    DOCUMENT = "document"
    OTHER = "other"

class IntentClassifier(BaseModel):
    intent: Intent = Field(description="The user's primary intent.")
    confidence: float = Field(ge=0,le=1,description="Confidence score between 0 and 1.")

class AppointmentState(TypedDict):
    treatment: str | None
    date: str | None
    time: str | None
    company_name: str
    appointment_id: str
    appointment_date: str
    appointment_status: str
    appointment: dict | None


class AestheticState(TypedDict):
    message: str
    classification: IntentClassifier
    patient_name: str | None
    phone_number: str | None
    company_name: str | None
    treatment: str | None
    appointment_date: str | None
    appointment_time: str | None
    appointment_status: str | None
    retrieved_documents: list
    response: str