from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from services.esim_provider import AVAILABLE_COUNTRIES, COUNTRY_NAMES, get_plans_by_country, ESIMPlan


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Купить eSIM"), KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="📦 Мои заказы"), KeyboardButton(text="🎁 Реферальная программа")],
            [KeyboardButton(text="❓ Как установить eSIM"), KeyboardButton(text="💬 Поддержка")],
        ],
        resize_keyboard=True,
    )


def countries_kb() -> InlineKeyboardMarkup:
    buttons = []
    for code in AVAILABLE_COUNTRIES:
        name = COUNTRY_NAMES.get(code, code)
        buttons.append(InlineKeyboardButton(text=name, callback_data=f"country:{code}"))
    rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    rows.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def plans_kb(country_code: str) -> InlineKeyboardMarkup:
    plans = get_plans_by_country(country_code)
    buttons = []
    for plan in plans:
        label = f"{plan.data_gb} ГБ / {plan.duration_days} дн. — {plan.price_eur}€"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"plan:{plan.plan_id}")])
    buttons.append([InlineKeyboardButton(text="◀️ Назад к странам", callback_data="back:countries")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_order_kb(plan_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить картой", callback_data=f"pay:stripe:{plan_id}")],
        [InlineKeyboardButton(text="💰 Оплатить с баланса", callback_data=f"pay:balance:{plan_id}")],
        [InlineKeyboardButton(text="◀️ Отмена", callback_data=f"back:country")],
    ])


def payment_kb(payment_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Перейти к оплате", url=payment_url)],
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="check_payment")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_order")],
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


def back_to_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back:main")]
    ])


def support_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Написать в поддержку", url="https://t.me/YOUR_SUPPORT_USERNAME")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back:main")],
    ])
