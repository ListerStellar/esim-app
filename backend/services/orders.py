import logging
from config import config
from database.crud import (
    get_user_by_telegram_id, get_user_by_id, create_order, set_order_paid,
    set_order_activated, update_user_balance, create_referral_bonus,
    get_order_by_id
)
from database.db import AsyncSessionLocal, User
from sqlalchemy import select
from services.esim_provider import get_plan_by_id, activate_esim
from services.payment import create_payment_link
from services.email import send_receipt_email

logger = logging.getLogger(__name__)

async def process_payment(order_id: int):
    """Активирует eSIM и начисляет бонусы после успешной оплаты."""
    order = await get_order_by_id(order_id)
    if not order or order.status != "paid":
        return None

    plan = await get_plan_by_id(order.plan_id)
    if not plan:
        return None

    try:
        # 1. Активация eSIM
        activation = await activate_esim(plan)
        await set_order_activated(
            order_id=order.id,
            iccid=activation.iccid,
            qr_code=activation.qr_code_base64,
            activation_code=activation.activation_code,
        )

        # 2. Начисление реферального бонуса
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.id == order.user_id))
            user_model = result.scalar_one_or_none()
            if user_model and user_model.referred_by:
                res_ref = await session.execute(select(User).where(User.id == user_model.referred_by))
                referrer = res_ref.scalar_one_or_none()
                if referrer:
                    bonus = config.REFERRAL_BONUS_EUR
                    await update_user_balance(referrer.id, bonus)
                    await create_referral_bonus(referrer.id, user_model.id, bonus)
                    
            # 3. Send email receipt
            if user_model and user_model.email:
                order_details = {
                    "country_name": order.country_name,
                    "data_gb": order.data_gb,
                    "duration_days": order.duration_days,
                    "esim_iccid": activation.iccid,
                    "esim_activation_code": activation.activation_code,
                    "esim_qr_code": activation.qr_code_base64,
                }
                await send_receipt_email(user_model.email, order_details)
        
        return await get_order_by_id(order_id)
    except Exception as e:
        logger.error(f"Failed to process payment for order {order_id}: {e}")
        return None

async def buy_with_balance_service(user_id: int, plan_id: str) -> dict:
    plan = await get_plan_by_id(plan_id)
    if not plan:
        return {"success": False, "error": "plan_not_found"}

    user = await get_user_by_id(user_id)
    if not user:
        return {"success": False, "error": "user_not_found"}

    if user.balance < plan.price_eur:
        return {"success": False, "error": f"insufficient_funds|{user.balance}|{plan.price_eur}"}

    # Списываем баланс и создаем заказ
    await update_user_balance(user.id, -plan.price_eur)
    order = await create_order(
        user_id=user.id,
        plan_id=plan.plan_id,
        country_code=plan.country_code,
        country_name=plan.country_name,
        data_gb=plan.data_gb,
        duration_days=plan.duration_days,
        price_eur=plan.price_eur,
    )
    await set_order_paid(order.id, payment_id="balance")
    
    activated_order = await process_payment(order.id)
    if not activated_order:
        from database.crud import set_order_failed
        await set_order_failed(order.id)
        return {"success": False, "error": "esim_activation_error"}
    
    return {
        "success": True, 
        "order_id": activated_order.id,
        "country_name": activated_order.country_name,
        "data_gb": activated_order.data_gb,
        "duration_days": activated_order.duration_days,
        "iccid": activated_order.esim_iccid,
        "activation_code": activated_order.esim_activation_code,
        "qr_code_base64": activated_order.esim_qr_code,
    }

async def buy_with_stripe_service(user_id: int, plan_id: str, redirect_url: str = None) -> dict:
    plan = await get_plan_by_id(plan_id)
    if not plan:
        return {"success": False, "error": "plan_not_found"}

    user = await get_user_by_id(user_id)
    if not user:
        return {"success": False, "error": "user_not_found"}

    order = await create_order(
        user_id=user.id,
        plan_id=plan.plan_id,
        country_code=plan.country_code,
        country_name=plan.country_name,
        data_gb=plan.data_gb,
        duration_days=plan.duration_days,
        price_eur=plan.price_eur,
    )

    if not config.STRIPE_SECRET_KEY or config.STRIPE_SECRET_KEY == "" or config.STRIPE_SECRET_KEY == "mock":
        await set_order_paid(order.id, payment_id="test_payment_mock")
        activated_order = await process_payment(order.id)
        if not activated_order:
            from database.crud import set_order_failed
            await set_order_failed(order.id)
            return {"success": False, "error": "esim_activation_error_test"}
        
        return {
            "success": True, 
            "mock": True,
            "order_id": activated_order.id,
            "country_name": activated_order.country_name,
            "data_gb": activated_order.data_gb,
            "duration_days": activated_order.duration_days,
            "iccid": activated_order.esim_iccid,
            "activation_code": activated_order.esim_activation_code,
            "qr_code_base64": activated_order.esim_qr_code,
        }

    try:
        payment_url = await create_payment_link(
            order_id=order.id,
            plan_name=f"{plan.country_name} {plan.data_gb}ГБ/{plan.duration_days}дн",
            price_eur=plan.price_eur,
            user_telegram_id=user.telegram_id,  # stripe metadata
            redirect_url=redirect_url,
        )
        return {"success": True, "mock": False, "payment_url": payment_url, "order_id": order.id, "price_eur": plan.price_eur}
    except Exception as e:
        logger.error(f"Payment gateway error: {e}")
        from database.crud import set_order_failed
        await set_order_failed(order.id)
        return {"success": False, "error": "payment_system_error"}

async def check_payment_service(order_id: int) -> dict:
    order = await get_order_by_id(order_id)
    if not order:
        return {"success": False, "error": "order_not_found"}
    
    if order.status == "activated":
        return {
            "success": True,
            "status": "activated",
            "order_id": order.id,
            "country_name": order.country_name,
            "data_gb": order.data_gb,
            "duration_days": order.duration_days,
            "iccid": order.esim_iccid,
            "activation_code": order.esim_activation_code,
            "qr_code_base64": order.esim_qr_code,
        }
    if order.status == "paid":
        activated_order = await process_payment(order_id)
        if not activated_order:
            return {"success": False, "error": "esim_activation_error"}
        return {
            "success": True,
            "status": "activated",
            "order_id": activated_order.id,
            "country_name": activated_order.country_name,
            "data_gb": activated_order.data_gb,
            "duration_days": activated_order.duration_days,
            "iccid": activated_order.esim_iccid,
            "activation_code": activated_order.esim_activation_code,
            "qr_code_base64": activated_order.esim_qr_code,
        }
        
    return {"success": True, "status": order.status}
