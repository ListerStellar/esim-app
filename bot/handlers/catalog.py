from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.kb import countries_kb, plans_kb, confirm_order_kb
from api_client import backend

router = Router()

class OrderState(StatesGroup):
    choosing_country = State()
    choosing_plan = State()
    confirming = State()

@router.message(F.text == "🌍 Купить eSIM")
async def show_catalog(message: Message, state: FSMContext):
    await state.set_state(OrderState.choosing_country)
    catalog = await backend.get_countries()
    await message.answer(
        "🌍 <b>Выбери страну</b>\n\nВ какой стране нужен интернет?",
        reply_markup=countries_kb(catalog.countries, catalog.names),
        parse_mode="HTML",
    )

@router.callback_query(F.data.startswith("country:"))
async def select_country(callback: CallbackQuery, state: FSMContext):
    country_code = callback.data.split(":")[1]
    
    catalog = await backend.get_countries()
    country_name = catalog.names.get(country_code, country_code)

    await state.update_data(country_code=country_code)
    await state.set_state(OrderState.choosing_plan)

    plans = await backend.get_plans_by_country(country_code)
    await callback.message.edit_text(
        f"📦 <b>Тарифы для {country_name}</b>\n\nВыбери подходящий пакет:",
        reply_markup=plans_kb(plans),
        parse_mode="HTML",
    )
    await callback.answer()

@router.callback_query(F.data.startswith("plan:"))
async def select_plan(callback: CallbackQuery, state: FSMContext):
    plan_id = callback.data.split(":")[1]
    plan = await backend.get_plan_by_id(plan_id)
    if not plan:
        await callback.answer("Тариф не найден", show_alert=True)
        return

    await state.update_data(plan_id=plan_id)
    await state.set_state(OrderState.confirming)

    text = (
        f"✅ <b>Подтверди заказ</b>\n\n"
        f"🌍 Страна: {plan.country_name}\n"
        f"📶 Данные: {plan.data_gb} ГБ\n"
        f"📅 Срок: {plan.duration_days} дней\n"
        f"💰 Цена: <b>{plan.price_eur}€</b>\n\n"
        f"ℹ️ После оплаты ты получишь QR-код для установки eSIM прямо здесь в боте."
    )

    await callback.message.edit_text(text, reply_markup=confirm_order_kb(plan_id), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "back:countries")
async def back_to_countries(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.choosing_country)
    catalog = await backend.get_countries()
    await callback.message.edit_text(
        "🌍 <b>Выбери страну</b>",
        reply_markup=countries_kb(catalog.countries, catalog.names),
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

    catalog = await backend.get_countries()
    country_name = catalog.names.get(country_code, country_code)

    await state.set_state(OrderState.choosing_plan)
    plans = await backend.get_plans_by_country(country_code)
    await callback.message.edit_text(
        f"📦 <b>Тарифы для {country_name}</b>\n\nВыбери подходящий пакет:",
        reply_markup=plans_kb(plans),
        parse_mode="HTML",
    )
    await callback.answer()
