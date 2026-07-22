from enum import Enum
from typing import TypedDict

from pydantic import BaseModel, Field

from pydantic import BaseModel


class AestheticRequest(BaseModel):
    message: str
    company_name: str | None = None
    phone_number: str | None = None
    
class AppointmentDetails(BaseModel):
    patient_name: str | None = Field(
        default=None,
        description="Patient's full name if mentioned.",
    )

    phone_number: str | None = Field(
        default=None,
        description="Patient's phone number if mentioned.",
    )

    treatment: str | None = Field(
        default=None,
        description="Treatment requested by the patient.",
    )

    # Existing appointment
    current_appointment_date: str | None = Field(
        default=None,
        description="Current appointment date in YYYY-MM-DD format.",
    )

    current_appointment_time: str | None = Field(
        default=None,
        description="Current appointment time in HH:MM format.",
    )

    # New appointment (booking/reschedule)
    new_appointment_date: str | None = Field(
        default=None,
        description="New appointment date in YYYY-MM-DD format.",
    )

    new_appointment_time: str | None = Field(
        default=None,
        description="New appointment time in HH:MM format.",
    )


class Intent(str, Enum):
    BOOKING = "booking"
    CONSULTATION = "consultation"
    APPOINTMENT = "request_appointment"
    RESCHEDULE = "reschedule"
    CANCELLATION = "cancellation"
    PRICING = "pricing"
    TREATMENT = "treatment"
    INFO = "info"
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


class IntentClassification(BaseModel):
    intent: Intent = Field(
        description="The user's primary intent."
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score between 0 and 1.",
    )


class AppointmentState(TypedDict):
    appointment_id: str
    company_name: str
    patient_name: str
    phone_number: str
    treatment: str
    appointment_date: str
    appointment_time: str
    appointment_status: str


class AestheticState(TypedDict):
    message: str
    classification: IntentClassification
    patient_name: str | None
    phone_number: str | None
    company_name: str | None
    treatment: str | None
    current_appointment_date: str | None
    current_appointment_time: str | None
    new_appointment_date: str | None
    new_appointment_time: str | None
    appointment: dict | None
    appointment_status: str | None

    # Knowledge Base
    retrieved_documents: list

    # Final response
    response: str
    error: str | None