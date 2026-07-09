from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from api_client import backend
from config import config

router = Router()


@router.message(F.text == "🎁 Реферальная программа")
async def show_referral(message: Message, bot: Bot):
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("Напиши /start для начала")
        return

    bot_info = await bot.get_me()
    bot_username = bot_info.username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user.referral_code}"
    ref_count = await backend.count_referrals(user.id)

    text = (
        f"🎁 <b>Реферальная программа</b>\n\n"
        f"Приглашай друзей и получай <b>{config.REFERRAL_BONUS_EUR}€</b> "
        f"на баланс за каждого, кто сделает первый заказ!\n\n"
        f"👥 Приглашено: <b>{ref_count}</b> человек\n"
        f"💰 Заработано: <b>{round(ref_count * config.REFERRAL_BONUS_EUR, 2)}€</b>\n\n"
        f"🔗 Твоя ссылка:\n<code>{ref_link}</code>\n\n"
        f"Нажми «Поделиться» чтобы отправить ссылку друзьям 👇"
    )

    share_text = (
        f"Советую eSIM Store — дешёвый мобильный интернет в 50+ странах!\n"
        f"Активация мгновенная, всё через Telegram.\n{ref_link}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📤 Поделиться ссылкой",
            url=f"https://t.me/share/url?url={ref_link}&text={share_text}",
        )],
    ])

    await message.answer(text, reply_markup=kb, parse_mode="HTML")
