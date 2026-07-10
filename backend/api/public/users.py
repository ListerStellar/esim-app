from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.db import get_session, User, Order
from auth.security import get_current_user, JWTUser

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
                "created_at": o.created_at
            }
            for o in orders
        ]
    }
