from langchain_openai import ChatOpenAI
from langgraph.types import Command

from app.agents.aesthetic.state.aesthic_state import AestheticState


async def GenerateResponse(state: AestheticState):
    print("Entering into Generating response...")
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
    )

    system_prompt = """
You are a professional AI receptionist for an aesthetic clinic.

Your job is to respond naturally on WhatsApp.

Guidelines:
- Be warm and professional.
- Keep replies concise.
- Never invent appointment details.
- If an appointment was scheduled, confirm it.
- If it was cancelled, acknowledge the cancellation.
- If it was rescheduled, mention the new date and time.
- If documentation was retrieved, answer ONLY using that information.
- If information is unavailable, politely say you don't know and offer to connect the patient with the clinic.
- Never mention databases, AI, or internal systems.
"""

    human_prompt = f"""
Patient Name:
{state.get("patient_name")}

User Message:
{state.get("message")}

Appointment Status:
{state.get("appointment_status")}

Appointment:
{state.get("appointment")}

Retrieved Documents:
{state.get("retrieved_documents")}

Generate the final WhatsApp response.
"""

    response = await llm.ainvoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt},
        ]
    )

    return Command(
        update={
            "response": response.content,
        },
        goto="END",
    )