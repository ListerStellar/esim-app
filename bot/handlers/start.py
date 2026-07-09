from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from api_client import backend
from keyboards.kb import main_menu_kb, language_kb

router = Router()

WELCOME_TEXT = {
    "ru": (
        "👋 Добро пожаловать в <b>eSIM Store</b>!\n\n"
        "🌍 Мобильный интернет в 50+ странах\n"
        "⚡️ Мгновенная активация — без очередей\n"
        "💰 Дешевле местных операторов до 3 раз\n\n"
        "Выбери язык / Choose language:"
    ),
    "cs": (
        "👋 Vítejte v <b>eSIM Store</b>!\n\n"
        "🌍 Mobilní internet ve 50+ zemích\n"
        "⚡️ Okamžitá aktivace\n"
        "💰 Levnější než místní operátoři\n\n"
        "Vyberte jazyk / Choose language:"
    ),
    "en": (
        "👋 Welcome to <b>eSIM Store</b>!\n\n"
        "🌍 Mobile internet in 50+ countries\n"
        "⚡️ Instant activation — no queues\n"
        "💰 Up to 3x cheaper than local carriers\n\n"
        "Choose language:"
    ),
}

MAIN_MENU_TEXT = {
    "ru": "🏠 <b>Главное меню</b>\n\nЧто хочешь сделать?",
    "cs": "🏠 <b>Hlavní menu</b>\n\nCo chceš udělat?",
    "en": "🏠 <b>Main Menu</b>\n\nWhat would you like to do?",
}


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    # Проверить параметры из /start deep link
    args = message.text.split()
    referral_code = None
    paid_order_id = None
    if len(args) > 1:
        param = args[1]
        if param.startswith("ref_"):
            referral_code = param[4:]
        elif param.startswith("paid_"):
            paid_order_id = param[5:]

    user = await backend.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        referral_code_used=referral_code,
    )

    if paid_order_id:
        res = await backend.check_payment(paid_order_id)
        if res.success and getattr(res, "status", "") == "activated":
            from handlers.order import send_esim_qr
            await message.answer("✅ Оплата подтверждена! Высылаем eSIM...")
            await send_esim_qr(message.bot, message.from_user.id, res)
            return
        elif res.success and getattr(res, "status", "") == "paid":
            await message.answer("⏳ Оплата получена, eSIM в процессе выпуска. Зайдите в 'Мои заказы' через пару минут.")
            return

    await message.answer(
        WELCOME_TEXT.get(user.language, WELCOME_TEXT["ru"]),
        reply_markup=language_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    await backend.set_user_language(callback.from_user.id, lang)

    text = MAIN_MENU_TEXT.get(lang, MAIN_MENU_TEXT["ru"])
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.message.answer(
        "✅ Язык выбран!" if lang == "ru" else ("✅ Language set!" if lang == "en" else "✅ Jazyk nastaven!"),
        reply_markup=main_menu_kb(),
    )
    await callback.answer()



