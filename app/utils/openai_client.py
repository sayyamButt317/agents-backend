from langfuse import Langfuse
from openai import OpenAI
from app.config import config


def get_openai_client():
    openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
    return openai_client


def get_langfuse_client():
    langfuse_client = Langfuse(
        public_key=config.LANGFUSE_PUBLIC_KEY,
        secret_key=config.LANGFUSE_SECRET_KEY,
        host=config.LANGFUSE_BASE_URL,
    )
    return langfuse_client


async def Whatsapp_Message_Generator(thread_id: str, msg_text: str, profile_name: str) -> str:
    response = get_openai_client().responses.create(
        model="gpt-5.5",
        input=[
            {
                "role": "user",
                "content": f"Thread ID: {thread_id}\nProfile Name: {profile_name}\nMessage Text: {msg_text}"
            }
        ]
    )
    return response.output_text