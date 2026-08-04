from fastapi import APIRouter, Request, HTTPException, Header
import stripe
from config import config
from database.crud import set_order_paid
from services.orders import process_payment
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhooks"])

@router.post("/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    if not config.STRIPE_WEBHOOK_SECRET or config.STRIPE_WEBHOOK_SECRET == "mock":
        return {"status": "ignored"}
        
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, config.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = getattr(session, "metadata", None)
        order_id_str = getattr(metadata, "order_id", None) if metadata else None
        
        if order_id_str:
            order_id = int(order_id_str)
            payment_id = getattr(session, "payment_intent", None)
            await set_order_paid(order_id, payment_id)
            await process_payment(order_id)

    return {"status": "success"}
