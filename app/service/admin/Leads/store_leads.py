import supabase
from app.core.exception import InternalServerErrorException
from app.schema.admin.leads_schema import Leads
from app.config.credentials_config import config
from app.db.connection import get_supabase

async def store_leads(leads: Leads) -> dict:
    try:
        supabase = get_supabase()
        result = supabase.table(config.SUPABASE_TABLE_LEADS).insert(leads.model_dump()).execute()
        inserted = result.data[0] if result.data else {}
        return inserted if isinstance(inserted, dict) else {}
    except Exception as e:
        print("Error:",e)
        raise InternalServerErrorException(message="Error storing leads")

async def GetallLeads():
    try:
        supabase = get_supabase()
        result = supabase.table(config.SUPABASE_TABLE_LEADS).select("*").execute()
        return result.data
    except Exception as e:
        print("Error:",e)
        raise InternalServerErrorException(message="Error getting Leads data")