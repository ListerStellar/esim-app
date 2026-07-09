from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from locales import get_text

def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(lang, "btn_buy")), KeyboardButton(text=get_text(lang, "btn_profile"))],
            [KeyboardButton(text=get_text(lang, "btn_orders")), KeyboardButton(text=get_text(lang, "btn_referral"))],
            [KeyboardButton(text=get_text(lang, "btn_install")), KeyboardButton(text=get_text(lang, "btn_support"))],
        ],
        resize_keyboard=True,
    )

def countries_kb(countries: list, names: dict, lang: str) -> InlineKeyboardMarkup:
    buttons = []
    for code in countries:
        name = names.get(code, code)
        buttons.append(InlineKeyboardButton(text=name, callback_data=f"country:{code}"))
    rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def plans_kb(plans: list, lang: str) -> InlineKeyboardMarkup:
    buttons = []
    for plan in plans:
        label = f"{plan.data_gb} GB / {plan.duration_days} d. — {plan.price_eur}€"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"plan:{plan.plan_id}")])
    buttons.append([InlineKeyboardButton(text=get_text(lang, "btn_back_countries"), callback_data="back:countries")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def confirm_order_kb(plan_id: str, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "btn_pay_card"), callback_data=f"pay:stripe:{plan_id}")],
        [InlineKeyboardButton(text=get_text(lang, "btn_pay_balance"), callback_data=f"pay:balance:{plan_id}")],
        [InlineKeyboardButton(text=get_text(lang, "btn_cancel"), callback_data=f"back:country")],
    ])

def payment_kb(payment_url: str, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "btn_go_pay"), url=payment_url)],
        [InlineKeyboardButton(text=get_text(lang, "btn_i_paid"), callback_data="check_payment")],
        [InlineKeyboardButton(text=get_text(lang, "btn_cancel"), callback_data="cancel_order")],
    ])

def language_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇨🇿 Čeština", callback_data="lang:cs"),
        ],
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang:uk"),
        ],
    ])

def support_kb(lang: str) -> InlineKeyboardMarkup:
    import os
    from config import config
    support_username = os.getenv("SUPPORT_USERNAME", config.BOT_USERNAME)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "btn_support"), url=f"https://t.me/{support_username}")],
    ])

def orders_kb(orders: list, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for order in orders[:10]:
        if order.status == "activated":
            builder.button(text=f"📲 QR #{order.id} ({order.country_name})", callback_data=f"esim_qr:{order.id}")
    builder.adjust(1)
    return builder.as_markup()
