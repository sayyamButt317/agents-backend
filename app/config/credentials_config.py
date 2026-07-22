import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


def env(key: str, default: str = "") -> str:
    return os.getenv(key, default)

class Config(BaseModel):
    SUPABASE_URL: str = Field(default=env("SUPABASE_URL"))
    SUPABASE_KEY: str = Field(default=env("SUPABASE_KEY"))

    DATABASE_URL: str = Field(default=env("DATABASE_URL"))
    DB_NAME: str = Field(default=env("MONGODB_ATLAS_DB_NAME"))

    OPENAI_API_KEY: str = Field(default=env("OPENAI_API_KEY"))
    OPENAI_MODEL_NAME: str = Field(default=env("OPENAI_MODEL_NAME"))

    PORT: int = Field(default=int(env("PORT", "8000")))

    RECIPENT_NUMBER: str = Field(default=env("RECIPENT_NUMBER"))
    WHATSAPP_PHONE_NUMBER: str = Field(default=env("WHATSAPP_PHONE_NUMBER"))
    META_APP_ID: str = Field(default=env("META_APP_ID"))
    META_WHATSAP_APP_SECRET: str = Field(default=env("META_WHATSAP_APP_SECRET"))
    META_WHATSAPP_ACCESSSTOKEN: str = Field(default=env("META_WHATSAPP_ACCESSSTOKEN"))
    WHATSAPP_BUSSINESS_ACCOUNT_ID: str = Field(
        default=env("WHATSAPP_BUSSINESS_ACCOUNT_ID")
    )
    WHATSAPP_GRAPH_API_VERSION: str = Field(default=env("WHATSAPP_GRAPH_API_VERSION"))

    LANGFUSE_SECRET_KEY: str = Field(default=env("LANGFUSE_SECRET_KEY"))
    LANGFUSE_PUBLIC_KEY: str = Field(default=env("LANGFUSE_PUBLIC_KEY"))
    LANGFUSE_BASE_URL: str = Field(default=env("LANGFUSE_BASE_URL"))

    META_VERIFY_TOKEN: str = Field(default=env("META_VERIFY_TOKEN"))
    META_APP_SECRET: str = Field(default=env("META_APP_SECRET"))
    PAGE_ACCESS_TOKEN: str = Field(default=env("PAGE_ACCESS_TOKEN"))

    REDIS_URL: str = Field(default=env("REDIS_URL"))
    MESSAGE_FROM: str = Field(default=env("MESSAGE_FROM"))

    SUPABASE_TABLE_BUSINESS_DETAILS: str = Field(
        default=env("SUPABASE_TABLE_BUSINESS_DETAILS", "businessDetails")
    )
    SUPABASE_TABLE_LEADS: str = Field(default=env("SUPABASE_TABLE_LEADS", "leads"))
    SUPABASE_TABLE_APPOINTMENT: str = Field(default=env("SUPABASE_TABLE_APPOINTMENT", "appointment"))


config = Config()
