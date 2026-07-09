from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from api_client import backend
from config import config
from locales import get_text

router = Router()


def is_admin(telegram_id: int) -> bool:
    return telegram_id in config.ADMIN_IDS


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    user = await backend.get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "en"

    stats = await backend.get_stats()
    text = get_text(
        lang, 
        "admin_panel",
        total_users=stats['total_users'],
        total_orders=stats['total_orders'],
        paid_orders=stats['paid_orders'],
        revenue=stats['revenue']
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("stats"))
async def admin_stats(message: Message):
    if not is_admin(message.from_user.id):
        return
        
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "en"
    
    stats = await backend.get_stats()
    text = get_text(
        lang,
        "admin_stats",
        total_users=stats['total_users'],
        total_orders=stats['total_orders'],
        paid_orders=stats['paid_orders'],
        revenue=stats['revenue']
    )
    await message.answer(text)


@router.message(Command("addbalance"))
async def add_balance(message: Message):
    if not is_admin(message.from_user.id):
        return
        
    user_admin = await backend.get_user_by_telegram_id(message.from_user.id)
    lang = user_admin.language if user_admin else "en"
    
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer(get_text(lang, "admin_addbalance_usage"))
        return
    try:
        user_tg_id = int(parts[1])
        amount = float(parts[2])
    except ValueError:
        await message.answer(get_text(lang, "admin_invalid_format"))
        return

    user = await backend.get_user_by_telegram_id(user_tg_id)
    if not user:
        await message.answer(get_text(lang, "admin_user_not_found"))
        return

    await backend.update_user_balance(user_tg_id, amount)
    await message.answer(get_text(lang, "admin_balance_added", name=user.full_name, amount=amount))
