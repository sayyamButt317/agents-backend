from fastapi import APIRouter
from app.meta.privacy_policy import get_privacy_policy
from app.meta.whatsapp_webhook import verify_webhook, verify_whatsapp_webhook


router = APIRouter()


router.add_api_route(
    path="/whatsapp-webhook",
    endpoint=verify_whatsapp_webhook,
    methods=["GET"],
    tags=["Meta"],
    name="verify_whatsapp_webhook",
)
router.add_api_route(
    path="/privacy-policy",
    endpoint=get_privacy_policy,
    methods=["GET"],
    tags=["Meta"],
)
router.add_api_route(
    path="/meta",
    endpoint=verify_webhook,
    methods=["GET"],
    tags=["Meta"],
)

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
