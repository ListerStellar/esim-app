import base64
import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from api_client import backend
from keyboards.kb import payment_kb
from locales import get_text, get_error_text

logger = logging.getLogger(__name__)
router = Router()


async def send_esim_qr(bot: Bot, telegram_id: int, data: dict, lang: str = "en"):
    """Вспомогательная функция для отправки QR кода"""
    qr_bytes = base64.b64decode(data.qr_code_base64)
    qr_file = BufferedInputFile(qr_bytes, filename="esim_qr.png")

    text = get_text(lang, "how_to_install_short", activation_code=data.activation_code, order_id=data.order_id, iccid=data.iccid)
    text = (
        f"{get_text(lang, 'esim_ready')}\n\n"
        f"{get_text(lang, 'country')} {data.country_name}\n"
        f"{get_text(lang, 'data_gb')} {data.data_gb} GB / {data.duration_days} d.\n\n"
        + text
    )

    await bot.send_photo(
        chat_id=telegram_id,
        photo=qr_file,
        caption=text,
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("pay:stripe:"))
async def pay_with_stripe(callback: CallbackQuery, state: FSMContext, bot: Bot):
    plan_id = callback.data.split(":")[2]
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"
    
    res = await backend.buy_with_stripe(user.id, plan_id)
    if not res.success:
        await callback.answer(get_error_text(lang, res.error), show_alert=True)
        return

    await state.update_data(pending_order_id=res.order_id)

    if getattr(res, "mock", False):
        await callback.message.edit_text(
            get_text(lang, "test_mode", order_id=res.order_id),
            parse_mode="HTML",
        )
        await send_esim_qr(bot, callback.from_user.id, res, lang)
        await state.clear()
        return

    await callback.message.edit_text(
        get_text(lang, "payment_invoice", order_id=res.order_id, price=res.price_eur),
        reply_markup=payment_kb(res.payment_url, lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pay:balance:"))
async def pay_with_balance(callback: CallbackQuery, state: FSMContext, bot: Bot):
    plan_id = callback.data.split(":")[2]
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"
    
    await callback.message.edit_text(get_text(lang, "payment_processing"), parse_mode="HTML")
    
    res = await backend.buy_with_balance(user.id, plan_id)
    if not res.success:
        err_msg = get_error_text(lang, res.error)
        await callback.message.edit_text(f"{get_text(lang, 'payment_error')} {err_msg}")
        await callback.answer()
        return

    await callback.message.delete() # Удаляем сообщение "Обрабатываем"
    await send_esim_qr(bot, callback.from_user.id, res, lang)
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "check_payment")
async def check_payment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    order_id = data.get("pending_order_id")
    
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"

    if not order_id:
        await callback.answer(get_text(lang, "order_not_found"), show_alert=True)
        return

    res = await backend.check_payment(order_id)
    
    if not res.success:
        await callback.answer(get_error_text(lang, res.error), show_alert=True)
        return

    if res.status == "activated":
        await callback.message.edit_text(get_text(lang, "payment_success"))
        await send_esim_qr(bot, callback.from_user.id, res, lang)
        await state.clear()
    else:
        await callback.answer(
            get_text(lang, "payment_wait"),
            show_alert=True,
        )


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"
    
    await state.clear()
    await callback.message.edit_text(
        get_text(lang, "order_cancelled"),
    )
    await callback.answer()
