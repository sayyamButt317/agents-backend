from enum import Enum
from pydantic import BaseModel


class Status(str, Enum):
    NOT_CONTACTED = "not_contacted"
    PITCHED = "pitched"
    REPLIED = "replied"
    MEETING_BOOKED = "meeting_booked"
    CLOSED_WON = "closed_won"
    NOT_INTERESTED = "not_interested"
    OTHER = "other"

class Leads(BaseModel):
    country: str | None = None
    agency: str | None = None
    ceo: str | None = None
    niche: str | None = None
    email: str | None = None
    status: Status
    notes: str | None = None
