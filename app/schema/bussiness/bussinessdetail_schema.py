from pydantic import BaseModel


class ConnectSocialAccounts(BaseModel):
    instagram: str
    facebook: str
    linkedin: str
    tiktok: str


class BussinesDetails(BaseModel):
    brand_name: str
    brand_description: str
    brand_website: str
    niche: str
    agent_name: str
    whatsapp_number: str
    email: str
    phone: str
    bussiness_hours: str
    connect_social_accounts: list[ConnectSocialAccounts]
