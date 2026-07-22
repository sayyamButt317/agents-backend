
from enum import Enum


class SenderType(str, Enum):
    USER = "USER"
    AI = "AI"
    HUMAN = "HUMAN"
    SYSTEM = "SYSTEM"

class AccountType(str, Enum):
    USER = "user"
    BUSINESS = "business"

class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    INTERACTIVE = "interactive"
    BUTTON_REPLY = "button_reply"
    LOCATION = "location"
    CONTACT = "contact"
    SYSTEM = "system"

    