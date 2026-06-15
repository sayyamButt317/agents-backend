import re
from functools import lru_cache

from fastapi import Depends
from supabase import Client, create_client

from app.config import config


@lru_cache
def get_supabase() -> Client:
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in the environment")
    if not re.match(r"^https?://", config.SUPABASE_URL):
        raise RuntimeError(
            "SUPABASE_URL must be the Supabase API URL "
            "(https://<project-ref>.supabase.co), not a PostgreSQL connection string. "
            "Use DATABASE_URL for the postgres:// connection string."
        )
    return create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


def connect() -> None:
    get_supabase()


def close() -> None:
    get_supabase.cache_clear()


def get_supabase_client() -> Client:
    return get_supabase()


SupabaseDep = Depends(get_supabase_client)
