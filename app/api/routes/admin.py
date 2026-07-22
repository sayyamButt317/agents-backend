from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel

from app.schema.admin.leads_schema import Leads
from app.schema.bussiness.bussinessdetail_schema import BussinesDetails
from app.service.BussinessInformation.storebussinesdetails import storebussinesdetails
from app.service.admin.Leads.store_leads import store_leads

router = APIRouter()


@router.post("/create-business-details")
async def create_business_details(business_details: BussinesDetails):
    return await storebussinesdetails(business_details)

@router.post("/create-leads")
async def create_leads(leads: Leads):
    return await store_leads(leads)