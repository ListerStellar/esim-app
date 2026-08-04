from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.db import get_session, User, Order
from auth.security import get_current_user, JWTUser
from pydantic import BaseModel, EmailStr
import os

class LanguageUpdate(BaseModel):
    language: str

class LinkEmailRequest(BaseModel):
    email: EmailStr
    password: str



router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
async def get_my_profile(jwt_user: JWTUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user_res = await session.execute(select(User).filter(User.id == jwt_user.id))
    user = user_res.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    result = await session.execute(
        select(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc())
    )
    orders = result.scalars().all()
    
    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "email": user.email,
        "balance": user.balance,
        "language": user.language,
        "referral_code": user.referral_code,
        "is_banned": user.is_banned,
        "orders": [
            {
                "id": o.id,
                "plan_id": o.plan_id,
                "country_name": o.country_name,
                "data_gb": o.data_gb,
                "duration_days": o.duration_days,
                "price_eur": o.price_eur,
                "status": o.status,
                "created_at": o.created_at,
                "esim_iccid": o.esim_iccid,
                "esim_activation_code": o.esim_activation_code,
                "esim_qr_code": o.esim_qr_code,
            }
            for o in orders
        ]
    }

@router.patch("/me/language")
async def update_language(req: LanguageUpdate, jwt_user: JWTUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user_res = await session.execute(select(User).filter(User.id == jwt_user.id))
    user = user_res.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.language = req.language
    await session.commit()
    return {"status": "ok", "language": user.language}

import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from database.db import EmailVerificationToken
from auth.security import get_password_hash
from services.email import send_verification_email

@router.post("/me/link/email")
async def link_email(req: LinkEmailRequest, jwt_user: JWTUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user_res = await session.execute(select(User).filter(User.id == jwt_user.id))
    user = user_res.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.email:
        raise HTTPException(status_code=400, detail="Account already has an email linked")
        
    # Check if email is used
    email_res = await session.execute(select(User).filter(User.email == req.email))
    if email_res.scalars().first():
        raise HTTPException(status_code=400, detail="Email is already in use by another account")
        
    user.email = req.email
    user.hashed_password = get_password_hash(req.password)
    user.is_email_verified = False
    
    # Generate verification token
    plain_token = secrets.token_urlsafe(32)
    hashed_token = hashlib.sha256(plain_token.encode()).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    
    verification = EmailVerificationToken(
        user_id=user.id,
        token=hashed_token,
        expires_at=expires_at
    )
    session.add(verification)
    await session.commit()
    
    # Send email
    await send_verification_email(user.email, plain_token)
    
    return {"status": "verification_required"}

from api.public.auth_routes import TelegramLoginRequest, verify_telegram_auth_data

@router.post("/me/link/telegram")
async def link_telegram(req: TelegramLoginRequest, jwt_user: JWTUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user_res = await session.execute(select(User).filter(User.id == jwt_user.id))
    user = user_res.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.telegram_id:
        raise HTTPException(status_code=400, detail="Account already has a Telegram linked")
        
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise HTTPException(status_code=500, detail="Bot token not configured")
        
    verify_telegram_auth_data(req, bot_token)
    
    # Check if telegram_id is used
    tg_res = await session.execute(select(User).filter(User.telegram_id == req.id))
    if tg_res.scalars().first():
        raise HTTPException(status_code=400, detail="Telegram account is already in use by another account")
        
    user.telegram_id = req.id
    if not user.username:
        user.username = req.username
    if not user.full_name:
        name_parts = [req.first_name]
        if req.last_name:
            name_parts.append(req.last_name)
        user.full_name = " ".join(name_parts)
        
    await session.commit()
    return {"status": "ok"}
