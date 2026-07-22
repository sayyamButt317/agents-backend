from langgraph.graph import START, END, StateGraph
from app.agents.aesthetic.Nodes.Intent_Classifier import IntentClassifier
from app.agents.aesthetic.Nodes.appointmentdetails_Extractor import AppointmentDetailsExtractor
from app.agents.aesthetic.Nodes.collectappointment_details import CollectAppointmentDetails
from app.agents.aesthetic.Nodes.schedule_appointment import ScheduleAppointment
from app.agents.aesthetic.Nodes.check_appointment import CheckAppointment
from app.agents.aesthetic.Nodes.cancel_appointment import CancelAppointment
from app.agents.aesthetic.Nodes.reschedule_appointment import RescheduleAppointment
from app.agents.aesthetic.Nodes.generate_response import GenerateResponse

from app.agents.aesthetic.state.aesthic_state import AestheticState


graph = StateGraph(AestheticState)

# Nodes
graph.add_node("intent_classifier", IntentClassifier)
graph.add_node("appointment_details_extractor", AppointmentDetailsExtractor)
graph.add_node("collect_appointment_details", CollectAppointmentDetails)

graph.add_node("schedule_appointment", ScheduleAppointment)
graph.add_node("check_appointment", CheckAppointment)
graph.add_node("cancel_appointment", CancelAppointment)
graph.add_node("reschedule_appointment", RescheduleAppointment)

graph.add_node("generate_response", GenerateResponse)


# Entry
graph.add_edge(START, "intent_classifier")

graph.add_edge("intent_classifier","appointment_details_extractor",)
graph.add_edge("appointment_details_extractor","collect_appointment_details",)

# Every business node finishes here
graph.add_edge("schedule_appointment","generate_response",)
graph.add_edge("check_appointment","generate_response",)
graph.add_edge("cancel_appointment","generate_response",)
graph.add_edge("reschedule_appointment","generate_response")

graph.add_edge(
    "generate_response",
    END,
)

aesthetic_graph_app = graph.compile()