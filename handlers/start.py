from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from database.crud import get_or_create_user, set_user_language
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

    # Проверить реферальный код из /start deep link
    args = message.text.split()
    referral_code = None
    if len(args) > 1:
        param = args[1]
        if param.startswith("ref_"):
            referral_code = param[4:]

    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        referral_code_used=referral_code,
    )

    await message.answer(
        WELCOME_TEXT.get(user.language, WELCOME_TEXT["ru"]),
        reply_markup=language_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    await set_user_language(callback.from_user.id, lang)

    text = MAIN_MENU_TEXT.get(lang, MAIN_MENU_TEXT["ru"])
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.message.answer(
        "✅ Язык выбран!" if lang == "ru" else ("✅ Language set!" if lang == "en" else "✅ Jazyk nastaven!"),
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "back:main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>",
        parse_mode="HTML",
    )
    await callback.answer()
