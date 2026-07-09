import base64
import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from api_client import backend
from keyboards.kb import payment_kb, back_to_menu_kb

logger = logging.getLogger(__name__)
router = Router()



async def send_esim_qr(bot: Bot, telegram_id: int, data: dict):
    """Вспомогательная функция для отправки QR кода"""
    qr_bytes = base64.b64decode(data.qr_code_base64)
    qr_file = BufferedInputFile(qr_bytes, filename="esim_qr.png")

    await bot.send_photo(
        chat_id=telegram_id,
        photo=qr_file,
        caption=(
            f"🎉 <b>Ваш eSIM готов!</b>\n\n"
            f"🌍 Страна: {data.country_name}\n"
            f"📶 Данные: {data.data_gb} ГБ / {data.duration_days} дней\n\n"
            f"📱 <b>Как установить:</b>\n"
            f"1. Откройте Настройки → Сотовая связь → Добавить eSIM\n"
            f"2. Выберите «Сканировать QR-код» и отсканируйте код выше\n"
            f"   — или введите код активации вручную:\n\n"
            f"<code>{data.activation_code}</code>\n\n"
            f"⚠️ eSIM активируется при первом использовании.\n"
            f"📋 Заказ #{data.order_id} | ICCID: <code>{data.iccid}</code>"
        ),
        parse_mode="HTML",
        reply_markup=back_to_menu_kb(),
    )


@router.callback_query(F.data.startswith("pay:stripe:"))
async def pay_with_stripe(callback: CallbackQuery, state: FSMContext, bot: Bot):
    plan_id = callback.data.split(":")[2]
    
    res = await backend.buy_with_stripe(callback.from_user.id, plan_id)
    if not res.success:
        await callback.answer(res.error, show_alert=True)
        return

    await state.update_data(pending_order_id=res.order_id)

    if getattr(res, "mock", False):
        await callback.message.edit_text(
            f"🧪 <b>Тестовый режим</b>\n\nСимулируем успешную оплату заказа #{res.order_id}...",
            parse_mode="HTML",
        )
        await send_esim_qr(bot, callback.from_user.id, res)
        await state.clear()
        return

    await callback.message.edit_text(
        f"💳 <b>Оплата заказа #{res.order_id}</b>\n\n"
        f"Сумма: <b>{res.price_eur}€</b>\n\n"
        f"Нажми кнопку ниже для перехода к оплате.\n"
        f"После оплаты нажми «Я оплатил».",
        reply_markup=payment_kb(res.payment_url),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pay:balance:"))
async def pay_with_balance(callback: CallbackQuery, state: FSMContext, bot: Bot):
    plan_id = callback.data.split(":")[2]
    
    await callback.message.edit_text("⏳ Обрабатываем платеж и выпускаем eSIM...", parse_mode="HTML")
    
    res = await backend.buy_with_balance(callback.from_user.id, plan_id)
    if not res.success:
        await callback.message.edit_text(f"❌ Ошибка: {res.error}", reply_markup=back_to_menu_kb())
        await callback.answer()
        return

    await callback.message.delete() # Удаляем сообщение "Обрабатываем"
    await send_esim_qr(bot, callback.from_user.id, res)
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "check_payment")
async def check_payment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    order_id = data.get("pending_order_id")

    if not order_id:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    res = await backend.check_payment(order_id)
    
    if not res.success:
        await callback.answer(res.error, show_alert=True)
        return

    if res.status == "activated":
        await callback.message.edit_text("✅ Оплата прошла успешно! Высылаем eSIM...")
        await send_esim_qr(bot, callback.from_user.id, res)
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
