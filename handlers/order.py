import base64
import logging
from io import BytesIO

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from database.crud import (
    get_user_by_telegram_id, create_order, set_order_paid,
    set_order_activated, update_user_balance, create_referral_bonus,
    get_order_by_id
)
from services.esim_provider import get_plan_by_id, activate_esim
from services.payment import create_payment_link
from keyboards.kb import payment_kb, back_to_menu_kb
from config import config

logger = logging.getLogger(__name__)
router = Router()


async def deliver_esim(bot: Bot, telegram_id: int, order_id: int):
    """Активирует eSIM и отправляет QR-код пользователю."""
    from database.crud import get_order_by_id
    order = await get_order_by_id(order_id)
    if not order or order.status not in ("paid", "pending"):
        return

    plan = get_plan_by_id(order.plan_id)
    if not plan:
        return

    try:
        activation = await activate_esim(plan)
        await set_order_activated(
            order_id=order.id,
            iccid=activation.iccid,
            qr_code=activation.qr_code_base64,
            activation_code=activation.activation_code,
        )

        # Отправить QR-код как фото
        qr_bytes = base64.b64decode(activation.qr_code_base64)
        qr_file = BufferedInputFile(qr_bytes, filename="esim_qr.png")

        await bot.send_photo(
            chat_id=telegram_id,
            photo=qr_file,
            caption=(
                f"🎉 <b>Ваш eSIM готов!</b>\n\n"
                f"🌍 Страна: {order.country_name}\n"
                f"📶 Данные: {order.data_gb} ГБ / {order.duration_days} дней\n\n"
                f"📱 <b>Как установить:</b>\n"
                f"1. Откройте Настройки → Сотовая связь → Добавить eSIM\n"
                f"2. Выберите «Сканировать QR-код» и отсканируй код выше\n"
                f"   — или вручную введи код активации:\n\n"
                f"<code>{activation.activation_code}</code>\n\n"
                f"⚠️ eSIM активируется при первом использовании.\n"
                f"📋 Заказ #{order.id} | ICCID: <code>{activation.iccid}</code>"
            ),
            parse_mode="HTML",
            reply_markup=back_to_menu_kb(),
        )

        # Начислить реферальный бонус рефереру
        user = await get_user_by_telegram_id(telegram_id)
        if user and user.referred_by:
            from database.db import AsyncSessionLocal, User
            from sqlalchemy import select
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(User).where(User.id == user.referred_by))
                referrer = result.scalar_one_or_none()
                if referrer:
                    bonus = config.REFERRAL_BONUS_EUR
                    await update_user_balance(referrer.telegram_id, bonus)
                    await create_referral_bonus(referrer.id, user.id, bonus)
                    await bot.send_message(
                        chat_id=referrer.telegram_id,
                        text=f"🎁 Вам начислен реферальный бонус <b>+{bonus}€</b> на баланс!",
                        parse_mode="HTML",
                    )

    except Exception as e:
        logger.error(f"Failed to activate eSIM for order {order_id}: {e}")
        await bot.send_message(
            chat_id=telegram_id,
            text=(
                "⚠️ Оплата прошла, но при активации eSIM возникла ошибка.\n"
                "Мы уже разбираемся! Обратитесь в поддержку с номером заказа: "
                f"<b>#{order_id}</b>"
            ),
            parse_mode="HTML",
        )


@router.callback_query(F.data.startswith("pay:stripe:"))
async def pay_with_stripe(callback: CallbackQuery, state: FSMContext, bot: Bot):
    plan_id = callback.data.split(":")[2]
    plan = get_plan_by_id(plan_id)
    if not plan:
        await callback.answer("Тариф не найден", show_alert=True)
        return

    user = await get_user_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer("Пользователь не найден", show_alert=True)
        return

    order = await create_order(
        user_id=user.id,
        plan_id=plan.plan_id,
        country_code=plan.country_code,
        country_name=plan.country_name,
        data_gb=plan.data_gb,
        duration_days=plan.duration_days,
        price_eur=plan.price_eur,
    )

    await state.update_data(pending_order_id=order.id)

    # В dev-режиме (без Stripe ключа) — симулируем оплату
    if not config.STRIPE_SECRET_KEY or config.STRIPE_SECRET_KEY == "":
        await callback.message.edit_text(
            f"🧪 <b>Тестовый режим</b>\n\n"
            f"Stripe не настроен. Симулируем успешную оплату заказа #{order.id}...",
            parse_mode="HTML",
        )
        await set_order_paid(order.id, payment_id="test_payment_mock")
        await deliver_esim(bot, callback.from_user.id, order.id)
        await state.clear()
        return

    payment_url = await create_payment_link(
        order_id=order.id,
        plan_name=f"{plan.country_name} {plan.data_gb}ГБ/{plan.duration_days}дн",
        price_eur=plan.price_eur,
        user_telegram_id=callback.from_user.id,
    )

    await callback.message.edit_text(
        f"💳 <b>Оплата заказа #{order.id}</b>\n\n"
        f"Сумма: <b>{plan.price_eur}€</b>\n\n"
        f"Нажми кнопку ниже для перехода к оплате.\n"
        f"После оплаты нажми «Я оплатил».",
        reply_markup=payment_kb(payment_url),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pay:balance:"))
async def pay_with_balance(callback: CallbackQuery, state: FSMContext, bot: Bot):
    plan_id = callback.data.split(":")[2]
    plan = get_plan_by_id(plan_id)
    user = await get_user_by_telegram_id(callback.from_user.id)

    if not plan or not user:
        await callback.answer("Ошибка", show_alert=True)
        return

    if user.balance < plan.price_eur:
        await callback.answer(
            f"❌ Недостаточно средств. Баланс: {user.balance}€, нужно {plan.price_eur}€",
            show_alert=True,
        )
        return

    order = await create_order(
        user_id=user.id,
        plan_id=plan.plan_id,
        country_code=plan.country_code,
        country_name=plan.country_name,
        data_gb=plan.data_gb,
        duration_days=plan.duration_days,
        price_eur=plan.price_eur,
    )

    await update_user_balance(callback.from_user.id, -plan.price_eur)
    await set_order_paid(order.id, payment_id="balance")

    await callback.message.edit_text(
        f"✅ <b>Оплачено с баланса!</b>\n\nАктивируем ваш eSIM...",
        parse_mode="HTML",
    )
    await deliver_esim(bot, callback.from_user.id, order.id)
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "check_payment")
async def check_payment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Ручная проверка после оплаты через Stripe (в production — через webhook)."""
    data = await state.get_data()
    order_id = data.get("pending_order_id")

    if not order_id:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    order = await get_order_by_id(order_id)
    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    if order.status == "activated":
        await callback.answer("eSIM уже активирован и отправлен!", show_alert=True)
        return

    if order.status == "paid":
        await callback.message.edit_text("⏳ Активируем eSIM...")
        await deliver_esim(bot, callback.from_user.id, order_id)
        await state.clear()
    else:
        await callback.answer(
            "⏳ Оплата ещё не получена. Подождите несколько секунд и попробуйте снова.",
            show_alert=True,
        )


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "❌ Заказ отменён. Деньги не были списаны.",
        reply_markup=back_to_menu_kb(),
    )
    await callback.answer()
