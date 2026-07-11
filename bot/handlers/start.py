from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from api_client import backend
from keyboards.kb import main_menu_kb, language_kb
from locales import get_text

router = Router()


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
            await message.answer(get_text(user.language, "payment_success"))
            await send_esim_qr(message.bot, message.from_user.id, res, user.language)
            return
        elif res.success and getattr(res, "status", "") == "paid":
            await message.answer(get_text(user.language, "payment_wait"))
            return

    await message.answer(
        get_text(user.language, "welcome"),
        reply_markup=language_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    if user:
        await backend.set_user_language(user.id, lang)

    text = get_text(lang, "main_menu")
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.message.answer(
        get_text(lang, "lang_set"),
        reply_markup=main_menu_kb(lang),
    )
    await callback.answer()
