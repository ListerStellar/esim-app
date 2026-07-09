from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from datetime import datetime
import base64
from aiogram.types import BufferedInputFile

from api_client import backend
from keyboards.kb import language_kb, orders_kb, support_kb
from locales import get_text, MENU_BTN_PROFILE, MENU_BTN_ORDERS, MENU_BTN_INSTALL, MENU_BTN_SUPPORT

router = Router()


@router.message(F.text.in_(MENU_BTN_PROFILE))
async def show_profile(message: Message):
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "en"
    
    if not user:
        await message.answer(get_text(lang, "profile_not_found"))
        return

    orders = await backend.get_user_orders(user.id)
    paid_count = sum(1 for o in orders if o.status in ("paid", "activated"))

    text = (
        f"{get_text(lang, 'profile_title')}\n\n"
        f"{get_text(lang, 'profile_id')} <code>{user.telegram_id}</code>\n"
        f"{get_text(lang, 'profile_name')} {user.full_name}\n"
        f"{get_text(lang, 'profile_balance')} <b>{user.balance}€</b>\n"
        f"{get_text(lang, 'profile_orders')} {paid_count}\n"
        f"{get_text(lang, 'profile_lang')} {user.language.upper()}\n\n"
        f"{get_text(lang, 'profile_ref')} <code>{user.referral_code}</code>"
    )

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "btn_lang"), callback_data="change_language")],
    ])

    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery):
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"
    
    # This text can be hardcoded here since it offers language choices
    await callback.message.edit_text(
        "🌐 Выбери язык / Choose language:",
        reply_markup=language_kb(),
    )
    await callback.answer()


@router.message(F.text.in_(MENU_BTN_ORDERS))
async def show_orders(message: Message):
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "en"
    
    if not user:
        await message.answer(get_text(lang, "profile_not_found"))
        return

    orders = await backend.get_user_orders(user.id)
    if not orders:
        await message.answer(
            get_text(lang, "orders_empty"),
            parse_mode="HTML",
        )
        return

    text = f"{get_text(lang, 'orders_title')}\n\n"

    for order in orders[:10]:
        emoji = get_text(lang, f"order_status_{order.status}")
        dt = datetime.fromisoformat(order.created_at) if isinstance(order.created_at, str) else order.created_at
        text += (
            f"{emoji} <b>#{order.id}</b> — {order.country_name}\n"
            f"   {order.data_gb} GB / {order.duration_days} d. — {order.price_eur}€\n"
            f"   {dt.strftime('%d.%m.%Y %H:%M')}\n\n"
        )

    await message.answer(text, reply_markup=orders_kb(orders, lang), parse_mode="HTML")


@router.callback_query(F.data.startswith("esim_qr:"))
async def show_esim_qr(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.split(":")[1])
    
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"
    
    if not user:
        return
        
    orders = await backend.get_user_orders(user.id)
    order = next((o for o in orders if o.id == order_id), None)
    
    if not order or order.status != "activated":
        await callback.answer(get_text(lang, "order_not_found"), show_alert=True)
        return
        
    qr_bytes = base64.b64decode(order.esim_qr_code)
    photo = BufferedInputFile(qr_bytes, filename=f"esim_qr_{order.id}.png")
    
    text = (
        f"{get_text(lang, 'esim_ready_2', order_id=order.id)}\n\n"
        f"{get_text(lang, 'country')} {order.country_name}\n"
        f"{get_text(lang, 'data_gb')} {order.data_gb} GB\n"
        f"{get_text(lang, 'duration')} {order.duration_days} d.\n\n"
        + get_text(lang, "qr_scan_text", iccid=order.esim_iccid, activation_code=order.esim_activation_code)
    )
    
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo, caption=text, parse_mode="HTML")
    await callback.answer()


@router.message(F.text.in_(MENU_BTN_INSTALL))
async def how_to_install(message: Message):
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "en"
    
    await message.answer(get_text(lang, "how_to_text"), parse_mode="HTML")


@router.message(F.text.in_(MENU_BTN_SUPPORT))
async def support(message: Message):
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "en"
    
    await message.answer(
        get_text(lang, "support_text"),
        reply_markup=support_kb(lang),
        parse_mode="HTML",
    )
