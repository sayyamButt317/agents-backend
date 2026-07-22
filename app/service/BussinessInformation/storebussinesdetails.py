from app.config.credentials_config import config
from app.core.exception import InternalServerErrorException
from app.db.connection import get_supabase
from app.schema.bussiness.bussinessdetail_schema import BussinesDetails


async def storebussinesdetails(bussinesdetails: BussinesDetails) -> dict:
    if not config.SUPABASE_TABLE_BUSINESS_DETAILS:
        raise InternalServerErrorException(
            message="SUPABASE_TABLE_BUSINESS_DETAILS is not configured"
        )

    try:
        supabase = get_supabase()
        result = (
            supabase.table(config.SUPABASE_TABLE_BUSINESS_DETAILS)
            .insert(bussinesdetails.model_dump())
            .execute()
        )
        inserted = result.data[0] if result.data else {}
        return inserted if isinstance(inserted, dict) else {}
    except Exception as e:
        print(f"Error storing bussines details: {e}")
        raise InternalServerErrorException(
            message=f"Error storing bussines details: {e}"
        ) from e
