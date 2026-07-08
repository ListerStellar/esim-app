from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database.crud import get_user_by_telegram_id, get_user_orders
from keyboards.kb import language_kb, back_to_menu_kb

router = Router()


@router.message(F.text == "👤 Профиль")
async def show_profile(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("Пользователь не найден. Напиши /start")
        return

    orders = await get_user_orders(user.id)
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
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back:main")],
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
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("Напиши /start для начала")
        return

    orders = await get_user_orders(user.id)
    if not orders:
        await message.answer(
            "📦 У тебя пока нет заказов.\n\nНажми <b>🌍 Купить eSIM</b> для начала!",
            reply_markup=back_to_menu_kb(),
            parse_mode="HTML",
        )
        return

    text = "📦 <b>История заказов</b>\n\n"
    STATUS_EMOJI = {
        "pending": "⏳",
        "paid": "💳",
        "activated": "✅",
        "failed": "❌",
    }

    for order in orders[:10]:  # последние 10
        emoji = STATUS_EMOJI.get(order.status, "❓")
        text += (
            f"{emoji} <b>#{order.id}</b> — {order.country_name}\n"
            f"   {order.data_gb} ГБ / {order.duration_days} дн. — {order.price_eur}€\n"
            f"   {order.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        )

    await message.answer(text, reply_markup=back_to_menu_kb(), parse_mode="HTML")


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
    await message.answer(text, reply_markup=back_to_menu_kb(), parse_mode="HTML")


@router.message(F.text == "💬 Поддержка")
async def support(message: Message):
    from keyboards.kb import support_kb
    await message.answer(
        "💬 <b>Поддержка</b>\n\n"
        "Работаем 9:00–21:00 (CET)\n"
        "Ответ обычно в течение 30 минут.\n\n"
        "Или напиши напрямую — @YOUR_SUPPORT_USERNAME",
        reply_markup=support_kb(),
        parse_mode="HTML",
    )
