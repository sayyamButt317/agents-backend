from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AnyMessage
import operator

class RealStateAgentState(TypedDict):
    user_message:  Annotated[list[AnyMessage], operator.add]
    language: str
    llm_calls:int


class PropertyDetails(TypedDict):
    property_type: str
    property_location: str
    property_price: str
    property_description: str
    property_images: list[str]
    property_videos: list[str]
    property_documents: list[str]
    property_amenities: list[str]
    property_features: list[str]

class LeadQualifier(TypedDict):
    budget:str
    bedroom:str
    area:str
    investmentType:str

