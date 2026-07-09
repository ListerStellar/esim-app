from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from api_client import backend
from keyboards.kb import language_kb

router = Router()


@router.message(F.text == "👤 Профиль")
async def show_profile(message: Message):
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("Пользователь не найден. Напиши /start")
        return

    orders = await backend.get_user_orders(user.id)
    paid_count = sum(1 for o in orders if o.status in ("paid", "activated"))

    text = (
        f"👤 <b>Профиль</b>\n\n"
        f"🆔 ID: <code>{user.telegram_id}</code>\n"
        f"👤 Имя: {user.full_name}\n"
        f"💰 Баланс: <b>{user.balance}€</b>\n"
        f"📦 Заказов: {paid_count}\n"
        f"🌐 Язык: {user.language.upper()}\n\n"
        f"🔑 Реферальный код: <code>{user.referral_code}</code>"
    )

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Сменить язык", callback_data="change_language")],
    ])

    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery):
    await callback.message.edit_text(
        "🌐 Выбери язык / Choose language:",
        reply_markup=language_kb(),
    )
    await callback.answer()


@router.message(F.text == "📦 Мои заказы")
async def show_orders(message: Message):
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("Напиши /start для начала")
        return

    orders = await backend.get_user_orders(user.id)
    if not orders:
        await message.answer(
            "📦 У тебя пока нет заказов.\n\nНажми <b>🌍 Купить eSIM</b> для начала!",
            parse_mode="HTML",
        )
        return

    from datetime import datetime
    text = "📦 <b>История заказов</b>\n\n"
    STATUS_EMOJI = {
        "pending": "⏳",
        "paid": "💳",
        "activated": "✅",
        "failed": "❌",
    }

    from keyboards.kb import orders_kb

    for order in orders[:10]:  # последние 10
        emoji = STATUS_EMOJI.get(order.status, "❓")
        dt = datetime.fromisoformat(order.created_at) if isinstance(order.created_at, str) else order.created_at
        text += (
            f"{emoji} <b>#{order.id}</b> — {order.country_name}\n"
            f"   {order.data_gb} ГБ / {order.duration_days} дн. — {order.price_eur}€\n"
            f"   {dt.strftime('%d.%m.%Y %H:%M')}\n\n"
        )

    await message.answer(text, reply_markup=orders_kb(orders), parse_mode="HTML")

from aiogram import Bot
@router.callback_query(F.data.startswith("esim_qr:"))
async def show_esim_qr(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.split(":")[1])
    
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    if not user:
        return
        
    orders = await backend.get_user_orders(user.id)
    order = next((o for o in orders if o.id == order_id), None)
    
    if not order or order.status != "activated":
        await callback.answer("Заказ не найден или еще не активирован", show_alert=True)
        return
        
    import base64
    from aiogram.types import BufferedInputFile
    
    qr_bytes = base64.b64decode(order.esim_qr_code)
    photo = BufferedInputFile(qr_bytes, filename=f"esim_qr_{order.id}.png")
    
    text = (
        f"✅ <b>Ваша eSIM #{order.id}</b>\n\n"
        f"🌍 <b>Страна:</b> {order.country_name}\n"
        f"📊 <b>Трафик:</b> {order.data_gb} ГБ\n"
        f"⏳ <b>Срок:</b> {order.duration_days} дней\n\n"
        f"📱 <b>ICCID:</b> <code>{order.esim_iccid}</code>\n"
        f"🔑 <b>Код активации:</b>\n<code>{order.esim_activation_code}</code>\n\n"
        f"Отсканируйте QR-код выше камерой телефона или введите код активации вручную."
    )
    
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo, caption=text, parse_mode="HTML")
    await callback.answer()


@router.message(F.text == "❓ Как установить eSIM")
async def how_to_install(message: Message):
    text = (
        "📱 <b>Как установить eSIM</b>\n\n"
        "<b>iPhone (iOS 12.1+):</b>\n"
        "1. Настройки → Сотовая связь\n"
        "2. Добавить сотовый план\n"
        "3. Сканируй QR-код\n\n"
        "<b>Android:</b>\n"
        "1. Настройки → Подключения → SIM-менеджер\n"
        "2. Добавить тарифный план / eSIM\n"
        "3. Сканируй QR-код\n\n"
        "<b>⚠️ Важно:</b>\n"
        "• Твой телефон должен поддерживать eSIM\n"
        "• Разблокирован от оператора (unlocked)\n"
        "• Нужен Wi-Fi или мобильный интернет для активации\n\n"
        "❓ Остались вопросы? Напиши в поддержку."
    )
    await message.answer(text, parse_mode="HTML")


@router.message(F.text == "💬 Поддержка")
async def support(message: Message):
    from keyboards.kb import support_kb
    await message.answer(
        "💬 <b>Поддержка</b>\n\n"
        "Работаем 9:00–21:00 (CET)\n"
        "Ответ обычно в течение 30 минут.\n\n",
        reply_markup=support_kb(),
        parse_mode="HTML",
    )
