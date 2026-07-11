import random
import string
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import AsyncSessionLocal, User, Order, ReferralBonus
from config import config


def generate_referral_code(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# ──────────────── Users ────────────────

async def get_or_create_user(
    telegram_id: int,
    username: Optional[str],
    full_name: str,
    referral_code_used: Optional[str] = None,
) -> User:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user:
            return user

        # Найти реферера если был код
        referrer_id = None
        if referral_code_used:
            ref_result = await session.execute(
                select(User).where(User.referral_code == referral_code_used)
            )
            referrer = ref_result.scalar_one_or_none()
            if referrer and referrer.telegram_id != telegram_id:
                referrer_id = referrer.id

        new_user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            referral_code=generate_referral_code(),
            referred_by=referrer_id,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()


async def get_user_by_id(user_id: int) -> Optional[User]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


async def update_user_balance(user_id: int, delta: float):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance = round(user.balance + delta, 2)
            await session.commit()


async def set_user_language(user_id: int, lang: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.language = lang
            await session.commit()


# ──────────────── Orders ────────────────

async def create_order(
    user_id: int,
    plan_id: str,
    country_code: str,
    country_name: str,
    data_gb: float,
    duration_days: int,
    price_eur: float,
) -> Order:
    async with AsyncSessionLocal() as session:
        order = Order(
            user_id=user_id,
            plan_id=plan_id,
            country_code=country_code,
            country_name=country_name,
            data_gb=data_gb,
            duration_days=duration_days,
            price_eur=price_eur,
        )
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order


async def get_order_by_id(order_id: int) -> Optional[Order]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()


async def set_order_paid(order_id: int, payment_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if order:
            order.status = "paid"
            order.payment_id = payment_id
            await session.commit()


async def set_order_failed(order_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if order:
            order.status = "failed"
            await session.commit()


async def set_order_activated(order_id: int, iccid: str, qr_code: str, activation_code: str):
    from datetime import datetime
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if order:
            order.status = "activated"
            order.esim_iccid = iccid
            order.esim_qr_code = qr_code
            order.esim_activation_code = activation_code
            order.activated_at = datetime.utcnow()
            await session.commit()


async def get_user_orders(user_id: int) -> list[Order]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
        )
        return result.scalars().all()


# ──────────────── Referrals ────────────────

async def count_referrals(user_id: int) -> int:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(func.count()).where(User.referred_by == user_id)
        )
        return result.scalar() or 0


async def create_referral_bonus(referrer_id: int, referred_id: int, amount: float):
    async with AsyncSessionLocal() as session:
        bonus = ReferralBonus(
            referrer_id=referrer_id,
            referred_id=referred_id,
            bonus_amount=amount,
        )
        session.add(bonus)
        await session.commit()


# ──────────────── Admin stats ────────────────

async def get_stats() -> dict:
    async with AsyncSessionLocal() as session:
        total_users = (await session.execute(select(func.count(User.id)))).scalar()
        total_orders = (await session.execute(select(func.count(Order.id)))).scalar()
        paid_orders = (await session.execute(
            select(func.count(Order.id)).where(Order.status.in_(["paid", "activated"]))
        )).scalar()
        revenue = (await session.execute(
            select(func.sum(Order.price_eur)).where(Order.status.in_(["paid", "activated"]))
        )).scalar() or 0.0

        return {
            "total_users": total_users,
            "total_orders": total_orders,
            "paid_orders": paid_orders,
            "revenue": round(revenue, 2),
        }
