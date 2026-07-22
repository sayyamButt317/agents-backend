from datetime import datetime, timezone
from fastapi import Request
from fastapi import HTTPException
from app.core.ws_manager import ws_manager
from app.service.save_message import save_conversation_message
from app.utils.enums import SenderType
from app.utils.message_context import get_history_list
from app.utils.openai_client import Whatsapp_Message_Generator


def extract_whatsapp_message(event: dict):
    entry = event.get("entry")
    if not entry:
        return None, None, None, None, None

    changes = entry[0].get("changes")
    if not changes:
        return None, None, None, None, None

    value = changes[0].get("value", {})
    messages = value.get("messages")
    if not messages:
        return None, None, None, None, None

    first_message = messages[0]
    thread_id = first_message.get("from")

    # Detect message type
    msg_type = first_message.get("type", "text")
    msg_text = ""

    if msg_type == "text":
        msg_text = first_message.get("text", {}).get("body", "")
    elif msg_type in ["image", "audio", "video", "document"]:
        # For media, we might still want to use the caption as msg_text if it exists
        msg_text = first_message.get(msg_type, {}).get("caption", "")

    profile_name = (
        value.get("contacts", [{}])[0].get("profile", {}).get("name") or "iShout"
    )

    return first_message, thread_id, msg_text, profile_name, value


async def process_incoming_message(thread_id, profile_name, msg_text):
    await save_conversation_message(
        thread_id=thread_id,
        username=profile_name,
        sender=SenderType.USER.value,
        message=msg_text,
    )

    await ws_manager.broadcast_event(
        "whatsapp.message",
        {
            "thread_id": thread_id,
            "sender": "USER",
            "message": msg_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
    


async def handle_whatsapp_events(request: Request):
    try:
        event = await request.json()
        first_message, thread_id, msg_text, profile_name, value = (
            extract_whatsapp_message(event)
        )
        if thread_id and msg_text and profile_name:
            response = await Whatsapp_Message_Generator(
                thread_id=thread_id,
                msg_text=msg_text,
                profile_name=profile_name
            )
        else:
            return None
        if response:
            await process_incoming_message(thread_id, profile_name, response)
            return response
    except Exception as e:
        print(f"[handle_whatsapp_events] Error in handle_whatsapp_events: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Webhook processing failed: {str(e)}"
        ) from e
