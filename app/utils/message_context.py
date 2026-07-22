import httpx
from app.config.credentials_config import config
from app.utils.printcolors import Colors



def build_message_context(last_messages: list[dict], latest: str) -> str:
    """
    Build conversation context for the AI reply.
    """

    history = "\n".join(
        f"{'AI' if msg.get('sender_type') == 'AI' else 'User'}: {msg.get('message', '')}"
        for msg in last_messages
    )

    return f"""
{NEGOTIATE_INFLUENCER_DM_PROMPT}

Conversation so far:
{history}

Latest message:
User: {latest}

Write the next reply as a natural human text message.
""".strip()


def build_whatsapp_message_context(last_messages: list[dict], latest: str) -> str:
    history = "\n".join(
        f"{'AI' if msg.get('sender_type') == 'AI' else 'User'}: {msg.get('message', '')}"
        for msg in last_messages
    )

    return f"""
{ANALYZE_INFLUENCER_WHATSAPP_PROMPT}

Conversation so far:
{history}

Latest message:
User: {latest}

Write the next reply as a natural WhatsApp message.
Keep it short, friendly, and human.
""".strip()


def normalize_ai_reply(reply) -> str:
    DEFAULT_REPLY = "Thanks for your message! Let me check and get back to you shortly."

    if isinstance(reply, GenerateReplyOutput):
        return reply.reply or DEFAULT_REPLY
    elif isinstance(reply, dict) and "reply" in reply:
        return reply["reply"] or DEFAULT_REPLY
    elif isinstance(reply, str):
        return reply or DEFAULT_REPLY
    else:
        return DEFAULT_REPLY


def get_history_list(state: dict) -> list:
    h = state.get("history")
    if isinstance(h, list):
        return h
    return []


def set_history_list(state: dict, history: list) -> None:
    state["history"] = history if isinstance(history, list) else []


def history_to_agent_messages(history: list[dict]) -> list[dict]:
    print(f"{Colors.BLUE}Enter int Agent memory History History{Colors.RESET}")
    recent_history = history[-20:] if isinstance(history, list) else []

    out = []
    for msg in recent_history:
        if not isinstance(msg, dict):
            continue
        role = (
            "user" if (msg.get("sender_type") or "").upper() == "USER" else "assistant"
        )
        content = (msg.get("message") or msg.get("content") or "").strip()
        if content:
            out.append({"role": role, "content": content})
    return out



async def upload_media_to_meta(
    file_bytes: bytes, mime_type: str, filename: str
) -> str | None:
    if not file_bytes:
        return None

    try:
        phone_number_id = "967002123161751"
        url = f"https://graph.facebook.com/v22.0/{phone_number_id}/media"
        headers = {
            "Authorization": f"Bearer {config.META_WHATSAPP_ACCESSSTOKEN}",
        }
        files = {"file": (filename, file_bytes, mime_type)}
        data = {
            "messaging_product": "whatsapp",
            "type": mime_type,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, data=data, files=files)

        response.raise_for_status()
        payload = response.json()
        media_id = payload.get("id")
        if not media_id:
            print(
                f"{Colors.RED}[upload_media_to_meta] No media id in response: {payload}"
            )
            return None
        return media_id
    except Exception as e:
        print(f"{Colors.RED}[upload_media_to_meta] Failed to upload media: {e}")
        return None
