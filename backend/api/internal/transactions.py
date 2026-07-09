from fastapi import APIRouter
from pydantic import BaseModel
from services.orders import buy_with_balance_service, buy_with_stripe_service, check_payment_service

router = APIRouter(prefix="/api/internal", tags=["transactions"])

class BuyRequest(BaseModel):
    telegram_id: int
    plan_id: str

@router.post("/buy_with_balance")
async def api_buy_with_balance(req: BuyRequest):
    return await buy_with_balance_service(req.telegram_id, req.plan_id)

@router.post("/buy_with_stripe")
async def api_buy_with_stripe(req: BuyRequest):
    return await buy_with_stripe_service(req.telegram_id, req.plan_id)

@router.get("/check_payment/{order_id}")
async def api_check_payment(order_id: int):
    return await check_payment_service(order_id)
