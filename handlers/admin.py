from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from database.crud import get_stats, get_user_by_telegram_id, update_user_balance
from config import config

router = Router()


def is_admin(telegram_id: int) -> bool:
    return telegram_id in config.ADMIN_IDS


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    stats = await get_stats()
    text = (
        f"🔧 <b>Админ-панель</b>\n\n"
        f"👥 Пользователей: <b>{stats['total_users']}</b>\n"
        f"📦 Заказов всего: <b>{stats['total_orders']}</b>\n"
        f"✅ Оплаченных: <b>{stats['paid_orders']}</b>\n"
        f"💰 Выручка: <b>{stats['revenue']}€</b>\n\n"
        f"<b>Команды:</b>\n"
        f"/stats — статистика\n"
        f"/addbalance [user_id] [amount] — пополнить баланс\n"
        f"/broadcast [text] — рассылка (скоро)\n"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("stats"))
async def admin_stats(message: Message):
    if not is_admin(message.from_user.id):
        return
    stats = await get_stats()
    await message.answer(
        f"📊 Пользователей: {stats['total_users']}\n"
        f"📦 Заказов: {stats['total_orders']}\n"
        f"✅ Оплачено: {stats['paid_orders']}\n"
        f"💰 Выручка: {stats['revenue']}€"
    )


@router.message(Command("addbalance"))
async def add_balance(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Использование: /addbalance [telegram_id] [сумма]")
        return
    try:
        user_tg_id = int(parts[1])
        amount = float(parts[2])
    except ValueError:
        await message.answer("Неверный формат")
        return

    user = await get_user_by_telegram_id(user_tg_id)
    if not user:
        await message.answer("Пользователь не найден")
        return

    await update_user_balance(user_tg_id, amount)
    await message.answer(f"✅ Пользователю {user.full_name} начислено {amount}€")
