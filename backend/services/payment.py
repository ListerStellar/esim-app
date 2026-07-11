"""
Stripe Payment Service
Документация: https://stripe.com/docs/api
"""

import stripe
from config import config

stripe.api_key = config.STRIPE_SECRET_KEY


async def create_payment_link(
    order_id: int,
    plan_name: str,
    price_eur: float,
    user_telegram_id: int,
    redirect_url: str = None,
) -> str:
    """
    Создаёт Stripe Checkout ссылку для оплаты.
    В production нужен реальный домен для success_url / cancel_url.
    """
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {"name": f"eSIM: {plan_name}"},
                "unit_amount": int(price_eur * 100),  # в центах
            },
            "quantity": 1,
        }],
        mode="payment",
        metadata={
            "order_id": str(order_id),
            "telegram_id": str(user_telegram_id),
        },
        success_url=f"{redirect_url}?order_id={order_id}" if redirect_url else f"https://t.me/{config.BOT_USERNAME}?start=paid_{order_id}",
        cancel_url=redirect_url if redirect_url else f"https://t.me/{config.BOT_USERNAME}?start=cancelled",
    )
    return session.url


async def verify_webhook(payload: bytes, sig_header: str) -> dict:
    """Верификация Stripe webhook события."""
    event = stripe.Webhook.construct_event(
        payload, sig_header, config.STRIPE_WEBHOOK_SECRET
    )
    return event
