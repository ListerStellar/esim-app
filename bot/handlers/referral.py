from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse

from api_client import backend
from config import config
from locales import get_text, MENU_BTN_REFERRAL

router = Router()


@router.message(F.text.in_(MENU_BTN_REFERRAL))
async def show_referral(message: Message, bot: Bot):
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "en"
    
    if not user:
        await message.answer(get_text(lang, "profile_not_found"))
        return

    bot_info = await bot.get_me()
    bot_username = bot_info.username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user.referral_code}"
    ref_count = await backend.count_referrals(user.id)

    earned = round(ref_count * config.REFERRAL_BONUS_EUR, 2)
    
    text = get_text(lang, "ref_title", bonus=config.REFERRAL_BONUS_EUR, count=ref_count, earned=earned, link=ref_link)
    share_text = get_text(lang, "ref_share", link=ref_link)

    # Encode share text for URL
    encoded_share_text = urllib.parse.quote(share_text)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text(lang, "btn_share"),
            url=f"https://t.me/share/url?url={ref_link}&text={encoded_share_text}",
        )],
    ])

    await message.answer(text, reply_markup=kb, parse_mode="HTML")
