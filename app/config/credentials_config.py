import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(override=True)


class Config(BaseModel):
    SUPABASE_URL: str = Field(default=os.getenv("SUPABASE_URL"))
    SUPABASE_KEY: str = Field(default=os.getenv("SUPABASE_KEY"))

    DATABASE_URL: str = Field(default=os.getenv("DATABASE_URL"))
    DB_NAME: str = Field(default=os.getenv("MONGODB_ATLAS_DB_NAME"))

    OPENAI_API_KEY: str = Field(default=os.getenv("OPENAI_API_KEY"))
    OPENAI_MODEL_NAME: str = Field(default=os.getenv("OPENAI_MODEL_NAME"))
    OPENAI_GPT_IMAGE_MODEL: str = Field(default=os.getenv("OPENAI_GPT_IMAGE_MODEL"))

    EMBEDDING_MODEL: str = Field(default=os.getenv("EMBEDDING_MODEL"))
    PORT: int = Field(default=int(os.getenv("PORT", "8000")))

    RECIPENT_NUMBER: str = Field(default=os.getenv("RECIPENT_NUMBER"))
    WHATSAPP_PHONE_NUMBER: str = Field(default=os.getenv("WHATSAPP_PHONE_NUMBER"))
    META_APP_ID: str = Field(default=os.getenv("META_APP_ID"))
    META_WHATSAP_APP_SECRET: str = Field(default=os.getenv("META_WHATSAP_APP_SECRET"))
    META_WHATSAPP_ACCESSSTOKEN: str = Field(
        default=os.getenv("META_WHATSAPP_ACCESSSTOKEN")
    )
    WHATSAPP_BUSSINESS_ACCOUNT_ID: str = Field(
        default=os.getenv("WHATSAPP_BUSSINESS_ACCOUNT_ID")
    )
    WHATSAPP_GRAPH_API_VERSION: str = Field(
        default=os.getenv("WHATSAPP_GRAPH_API_VERSION")
    )

    LANGFUSE_SECRET_KEY: str = Field(default=os.getenv("LANGFUSE_SECRET_KEY"))
    LANGFUSE_PUBLIC_KEY: str = Field(default=os.getenv("LANGFUSE_PUBLIC_KEY"))
    LANGFUSE_BASE_URL: str = Field(default=os.getenv("LANGFUSE_BASE_URL"))

    META_VERIFY_TOKEN: str = Field(default=os.getenv("META_VERIFY_TOKEN"))
    META_APP_SECRET: str = Field(default=os.getenv("META_APP_SECRET"))
    PAGE_ACCESS_TOKEN: str = Field(default=os.getenv("PAGE_ACCESS_TOKEN"))

    REDIS_URL: str = Field(default=os.getenv("REDIS_URL"))
    MESSAGE_FROM: str = Field(default=os.getenv("MESSAGE_FROM"))


# config singleton instance
config = Config()
