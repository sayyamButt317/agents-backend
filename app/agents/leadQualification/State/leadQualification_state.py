from enum import Enum
from typing import TypedDict, NotRequired


class QualificationLeadStatus(str, Enum):
    HOT_LEAD = "HOT_LEAD"
    WARM_LEAD = "WARM_LEAD"
    COLD_LEAD = "COLD_LEAD"
    UNQUALIFIED = "UNQUALIFIED"
    QUALIFIED = "QUALIFIED"


class WorkflowStatus(str, Enum):
    INITIAL = "INITIAL"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class SaveLeadDetails(TypedDict):
    leadId: str
    leadName: str
    leadEmail: str
    leadPhone: str
    leadAddress: str
    leadCity: str
    leadRegion: str
    leadSource: str
    leadStatus: QualificationLeadStatus


class ScoreLeadDetails(TypedDict):
    leadScore: float
    leadScoreReason: str
    leadScoreStatus: QualificationLeadStatus

initial_state: LeadQualificationState = {
    "workflowStatus": WorkflowStatus.INITIAL,
    "escalation": False,
    "notifySalesTeam": False,
    "sendFollowUpEmail": False,
}

class LeadQualificationState(TypedDict):
    workflowStatus: WorkflowStatus
    classifyLeadState: NotRequired[QualificationLeadStatus]
    escalation: bool
    notifySalesTeam: bool
    saveLeadDetails: NotRequired[SaveLeadDetails]
    scoreLeadDetails: NotRequired[ScoreLeadDetails]
    sendFollowUpEmail: bool