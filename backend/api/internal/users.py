from fastapi import APIRouter, HTTPException, Body
from typing import Optional
from pydantic import BaseModel
from database.crud import (
    get_or_create_user, get_user_by_telegram_id, update_user_balance,
    set_user_language, get_user_orders, count_referrals, get_stats
)

router = APIRouter(prefix="/api/internal/users", tags=["users"])

class UserCreate(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    full_name: str
    referral_code_used: Optional[str] = None

@router.post("")
async def api_get_or_create_user(data: UserCreate):
    return await get_or_create_user(data.telegram_id, data.username, data.full_name, data.referral_code_used)

@router.get("/{telegram_id}")
async def api_get_user(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.patch("/{user_id}/balance")
async def api_update_balance(user_id: int, delta: float = Body(..., embed=True)):
    return await update_user_balance(user_id, delta)

@router.patch("/{user_id}/language")
async def api_set_language(user_id: int, language: str = Body(..., embed=True)):
    return await set_user_language(user_id, language)

@router.get("/{user_id}/orders")
async def api_get_user_orders(user_id: int):
    return await get_user_orders(user_id)

@router.get("/{user_id}/referrals/count")
async def api_count_referrals(user_id: int):
    count = await count_referrals(user_id)
    return {"count": count}

@router.get("/system/stats")
async def api_get_stats():
    return await get_stats()
