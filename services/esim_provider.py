"""
eSIM Provider Service
=====================
Сейчас работает в режиме mock (тестовые данные).
Чтобы подключить реального поставщика:
  - Установи ESIM_PROVIDER=airalo или ESIM_PROVIDER=esimgo в .env
  - Добавь ESIM_API_KEY и ESIM_API_URL
"""

from dataclasses import dataclass
from typing import Optional
import httpx
import base64
import qrcode
from io import BytesIO

from config import config


@dataclass
class ESIMPlan:
    plan_id: str
    country_code: str
    country_name: str
    country_flag: str
    data_gb: float
    duration_days: int
    price_eur: float
    description: str


@dataclass
class ESIMActivation:
    iccid: str
    activation_code: str
    qr_code_base64: str


# ─────────────────────────────────────────────
# Каталог тарифов (mock — заменить на API-вызов)
# ─────────────────────────────────────────────
PLANS: list[ESIMPlan] = [
    # Чехия
    ESIMPlan("cz_1gb_7d",  "CZ", "Чехия 🇨🇿", "🇨🇿", 1,  7,  2.9,  "1 ГБ / 7 дней"),
    ESIMPlan("cz_3gb_14d", "CZ", "Чехия 🇨🇿", "🇨🇿", 3,  14, 5.9,  "3 ГБ / 14 дней"),
    ESIMPlan("cz_5gb_30d", "CZ", "Чехия 🇨🇿", "🇨🇿", 5,  30, 8.9,  "5 ГБ / 30 дней"),
    ESIMPlan("cz_10gb_30d","CZ", "Чехия 🇨🇿", "🇨🇿", 10, 30, 14.9, "10 ГБ / 30 дней"),
    # Европа (мультистрана)
    ESIMPlan("eu_3gb_15d", "EU", "Европа 🇪🇺", "🇪🇺", 3,  15, 7.9,  "3 ГБ / 15 дней • 30+ стран"),
    ESIMPlan("eu_5gb_30d", "EU", "Европа 🇪🇺", "🇪🇺", 5,  30, 12.9, "5 ГБ / 30 дней • 30+ стран"),
    ESIMPlan("eu_10gb_30d","EU", "Европа 🇪🇺", "🇪🇺", 10, 30, 19.9, "10 ГБ / 30 дней • 30+ стран"),
    ESIMPlan("eu_20gb_30d","EU", "Европа 🇪🇺", "🇪🇺", 20, 30, 29.9, "20 ГБ / 30 дней • 30+ стран"),
    # Германия
    ESIMPlan("de_3gb_14d", "DE", "Германия 🇩🇪", "🇩🇪", 3,  14, 5.9,  "3 ГБ / 14 дней"),
    ESIMPlan("de_10gb_30d","DE", "Германия 🇩🇪", "🇩🇪", 10, 30, 15.9, "10 ГБ / 30 дней"),
    # Польша
    ESIMPlan("pl_3gb_14d", "PL", "Польша 🇵🇱", "🇵🇱", 3,  14, 4.9,  "3 ГБ / 14 дней"),
    ESIMPlan("pl_10gb_30d","PL", "Польша 🇵🇱", "🇵🇱", 10, 30, 12.9, "10 ГБ / 30 дней"),
    # Словакия
    ESIMPlan("sk_3gb_14d", "SK", "Словакия 🇸🇰", "🇸🇰", 3,  14, 4.9,  "3 ГБ / 14 дней"),
    # Австрия
    ESIMPlan("at_5gb_30d", "AT", "Австрия 🇦🇹", "🇦🇹", 5,  30, 10.9, "5 ГБ / 30 дней"),
    # США
    ESIMPlan("us_3gb_15d", "US", "США 🇺🇸", "🇺🇸", 3,  15, 9.9,  "3 ГБ / 15 дней"),
    ESIMPlan("us_10gb_30d","US", "США 🇺🇸", "🇺🇸", 10, 30, 22.9, "10 ГБ / 30 дней"),
]

AVAILABLE_COUNTRIES = sorted(set(p.country_code for p in PLANS))
COUNTRY_NAMES = {p.country_code: p.country_name for p in PLANS}


def get_plans_by_country(country_code: str) -> list[ESIMPlan]:
    return [p for p in PLANS if p.country_code == country_code]


def get_plan_by_id(plan_id: str) -> Optional[ESIMPlan]:
    return next((p for p in PLANS if p.plan_id == plan_id), None)


# ─────────────────────────────────────────────
# Генерация QR-кода
# ─────────────────────────────────────────────
def generate_qr_bytes(data: str) -> bytes:
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ─────────────────────────────────────────────
# Mock провайдер (для разработки и тестирования)
# ─────────────────────────────────────────────
async def mock_activate_esim(plan: ESIMPlan) -> ESIMActivation:
    iccid = f"8901{plan.country_code}{'0' * 10}{plan.plan_id[-3:]}"[:20]
    activation_code = f"LPA:1$mock.esim.test$MOCK-{plan.plan_id.upper()}-ABC123"
    qr_bytes = generate_qr_bytes(activation_code)
    qr_b64 = base64.b64encode(qr_bytes).decode()
    return ESIMActivation(
        iccid=iccid,
        activation_code=activation_code,
        qr_code_base64=qr_b64,
    )


# ─────────────────────────────────────────────
# Airalo API (раскомментировать после регистрации)
# ─────────────────────────────────────────────
async def airalo_activate_esim(plan: ESIMPlan) -> ESIMActivation:
    """
    Документация: https://partners.airalo.com/api
    Нужно: ESIM_API_KEY, ESIM_API_URL=https://sandbox-partners-api.airalo.com
    """
    async with httpx.AsyncClient() as client:
        # 1. Получить токен
        auth_resp = await client.post(
            f"{config.ESIM_API_URL}/v2/token",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"Bearer {config.ESIM_API_KEY}"}
        )
        token = auth_resp.json()["data"]["access_token"]

        # 2. Купить eSIM
        order_resp = await client.post(
            f"{config.ESIM_API_URL}/v2/orders",
            json={"quantity": 1, "package_id": plan.plan_id},
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        esim_data = order_resp.json()["data"]["sims"][0]
        activation_code = esim_data["activation_code"]
        iccid = esim_data["iccid"]
        qr_bytes = generate_qr_bytes(activation_code)
        qr_b64 = base64.b64encode(qr_bytes).decode()

        return ESIMActivation(iccid=iccid, activation_code=activation_code, qr_code_base64=qr_b64)


# ─────────────────────────────────────────────
# eSIM Go API (раскомментировать после регистрации)
# ─────────────────────────────────────────────
async def esimgo_activate_esim(plan: ESIMPlan) -> ESIMActivation:
    """
    Документация: https://docs.esim-go.com
    Нужно: ESIM_API_KEY, ESIM_API_URL=https://api.esim-go.com
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{config.ESIM_API_URL}/v2.3/esim",
            json={"type": "transaction", "assign": [{"type": "bundle", "item": plan.plan_id, "quantity": 1}]},
            headers={"X-API-Key": config.ESIM_API_KEY}
        )
        esim = resp.json()["esims"][0]
        activation_code = esim["matchingId"]
        iccid = esim["iccid"]
        qr_bytes = generate_qr_bytes(f"LPA:1${esim['smdpAddress']}${activation_code}")
        qr_b64 = base64.b64encode(qr_bytes).decode()

        return ESIMActivation(iccid=iccid, activation_code=activation_code, qr_code_base64=qr_b64)


# ─────────────────────────────────────────────
# Основная функция активации (выбирает провайдера)
# ─────────────────────────────────────────────
async def activate_esim(plan: ESIMPlan) -> ESIMActivation:
    if config.ESIM_PROVIDER == "airalo":
        return await airalo_activate_esim(plan)
    elif config.ESIM_PROVIDER == "esimgo":
        return await esimgo_activate_esim(plan)
    else:
        return await mock_activate_esim(plan)
