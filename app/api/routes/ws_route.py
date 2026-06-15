from fastapi import APIRouter

from app.meta.whatsapp_webhook import verify_whatsapp_webhook

router = APIRouter()


router.add_api_route(
    path="/whatsapp-webhook",
    endpoint=verify_whatsapp_webhook,
    methods=["GET"],
    tags=["Meta"],
    name="verify_whatsapp_webhook",
)
# router.add_api_route(
#     path="/whatsapp-webhook",
#     endpoint=handle_whatsapp_events,
#     methods=["POST"],
#     tags=["Meta"],
#     name="handle_whatsapp_events",
# )
