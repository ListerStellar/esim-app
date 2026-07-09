from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.kb import countries_kb, plans_kb, confirm_order_kb
from api_client import backend
from locales import get_text, MENU_BTN_BUY

router = Router()

class OrderState(StatesGroup):
    choosing_country = State()
    choosing_plan = State()
    confirming = State()

@router.message(F.text.in_(MENU_BTN_BUY))
async def show_catalog(message: Message, state: FSMContext):
    user = await backend.get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "en"
    
    await state.set_state(OrderState.choosing_country)
    catalog = await backend.get_countries()
    await message.answer(
        get_text(lang, "choose_country"),
        reply_markup=countries_kb(catalog.countries, catalog.names, lang),
        parse_mode="HTML",
    )

@router.callback_query(F.data.startswith("country:"))
async def select_country(callback: CallbackQuery, state: FSMContext):
    country_code = callback.data.split(":")[1]
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"
    
    catalog = await backend.get_countries()
    country_name = catalog.names.get(country_code, country_code)

    await state.update_data(country_code=country_code)
    await state.set_state(OrderState.choosing_plan)

    plans = await backend.get_plans_by_country(country_code)
    await callback.message.edit_text(
        get_text(lang, "choose_plan", country=country_name),
        reply_markup=plans_kb(plans, lang),
        parse_mode="HTML",
    )
    await callback.answer()

@router.callback_query(F.data.startswith("plan:"))
async def select_plan(callback: CallbackQuery, state: FSMContext):
    plan_id = callback.data.split(":")[1]
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"
    
    plan = await backend.get_plan_by_id(plan_id)
    if not plan:
        await callback.answer(get_text(lang, "order_not_found"), show_alert=True)
        return

    await state.update_data(plan_id=plan_id)
    await state.set_state(OrderState.confirming)

    text = (
        f"✅ <b>Подтверди заказ</b>\n\n"
        f"{get_text(lang, 'country')} {plan.country_name}\n"
        f"{get_text(lang, 'data_gb')} {plan.data_gb} GB\n"
        f"{get_text(lang, 'duration')} {plan.duration_days} d.\n"
        f"💰 Цена: <b>{plan.price_eur}€</b>\n\n"
        f"ℹ️ После оплаты ты получишь QR-код для установки eSIM прямо здесь в боте."
    )

    await callback.message.edit_text(text, reply_markup=confirm_order_kb(plan_id, lang), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "back:countries")
async def back_to_countries(callback: CallbackQuery, state: FSMContext):
    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"
    
    await state.set_state(OrderState.choosing_country)
    catalog = await backend.get_countries()
    await callback.message.edit_text(
        get_text(lang, "choose_country"),
        reply_markup=countries_kb(catalog.countries, catalog.names, lang),
        parse_mode="HTML",
    )
    await callback.answer()

@router.callback_query(F.data == "back:country")
async def back_to_country(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    country_code = data.get("country_code")
    if not country_code:
        await back_to_countries(callback, state)
        return

    user = await backend.get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "en"
    
    catalog = await backend.get_countries()
    country_name = catalog.names.get(country_code, country_code)

    await state.set_state(OrderState.choosing_plan)
    plans = await backend.get_plans_by_country(country_code)
    await callback.message.edit_text(
        get_text(lang, "choose_plan", country=country_name),
        reply_markup=plans_kb(plans, lang),
        parse_mode="HTML",
    )
    await callback.answer()
