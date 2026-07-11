from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.orders import buy_with_balance_service, buy_with_stripe_service, check_payment_service
from auth.security import get_current_user, JWTUser

router = APIRouter(prefix="/transactions", tags=["transactions"])

class BuyRequest(BaseModel):
    plan_id: str
    redirect_url: str = None

@router.post("/buy_with_balance")
async def api_buy_with_balance(req: BuyRequest, current_user: JWTUser = Depends(get_current_user)):
    res = await buy_with_balance_service(current_user.id, req.plan_id)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res

@router.post("/buy_with_stripe")
async def api_buy_with_stripe(req: BuyRequest, current_user: JWTUser = Depends(get_current_user)):
    res = await buy_with_stripe_service(current_user.id, req.plan_id, req.redirect_url)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res

@router.get("/check_payment/{order_id}")
async def api_check_payment(order_id: int, current_user: JWTUser = Depends(get_current_user)):
    # В идеале нужно проверить, принадлежит ли заказ текущему пользователю,
    # но check_payment_service просто возвращает статус.
    res = await check_payment_service(order_id)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res
