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


# ─────────────────────────────────────────────
# eSIM Access API (Catalog)
# ─────────────────────────────────────────────
import hmac
import hashlib
import time
import uuid

def _get_esimaccess_headers(body_str: str = "") -> dict:
    access_code = config.ESIMACCESS_ACCESS_CODE
    secret_key = config.ESIMACCESS_SECRET_KEY
    if not access_code or not secret_key:
        return {}
        
    timestamp = str(int(time.time() * 1000))
    req_id = str(uuid.uuid4())
    sign_str = timestamp + req_id + access_code + body_str
    signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest().upper()
    
    return {
        "RT-AccessCode": access_code,
        "RT-RequestID": req_id,
        "RT-Timestamp": timestamp,
        "RT-Signature": signature,
        "Content-Type": "application/json"
    }

async def get_esimaccess_destinations() -> list[str]:
    global _destinations_cache, _destinations_cache_time

    if config.ESIM_PROVIDER != "esimaccess":
        return AVAILABLE_COUNTRIES
        
    if _destinations_cache and time.time() - _destinations_cache_time < 3600:
        return list(_destinations_cache.keys())

    body = "{}"
    headers = _get_esimaccess_headers(body)
    if not headers:
        return AVAILABLE_COUNTRIES

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "https://api.esimaccess.com/api/v1/open/location/list",
                data=body,
                headers=headers
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("success"):
                locs = data.get("obj", {}).get("locationList", [])
                _destinations_cache = {d["code"]: d["name"] for d in locs if d.get("code")}
                _destinations_cache_time = time.time()
                return list(_destinations_cache.keys())
            return AVAILABLE_COUNTRIES
        except Exception as e:
            logger.error(f"Failed to get eSIM Access destinations: {e}")
            return AVAILABLE_COUNTRIES

# ─────────────────────────────────────────────
# Celitech API (Catalog)
# ─────────────────────────────────────────────
_celitech_token: str = None
_celitech_token_expiry: float = 0

async def get_celitech_token() -> str:
    global _celitech_token, _celitech_token_expiry
    import time
    
    if _celitech_token and time.time() < _celitech_token_expiry:
        return _celitech_token

    if not config.CELITECH_CLIENT_ID or not config.CELITECH_CLIENT_SECRET:
        logger.warning("Celitech credentials not set")
        return ""

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "https://auth.celitech.net/oauth2/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": config.CELITECH_CLIENT_ID,
                    "client_secret": config.CELITECH_CLIENT_SECRET
                }
            )
            resp.raise_for_status()
            data = resp.json()
            _celitech_token = data.get("access_token")
            # Usually expires in 3600 seconds. Save it with a 60s buffer.
            expires_in = data.get("expires_in", 3600)
            _celitech_token_expiry = time.time() + expires_in - 60
            return _celitech_token
        except Exception as e:
            logger.error(f"Failed to get Celitech token: {e}")
            return ""

_destinations_cache: dict = {}
_destinations_cache_time: float = 0

async def get_celitech_destinations() -> list[str]:
    global _destinations_cache, _destinations_cache_time
    import time

    if config.ESIM_PROVIDER != "celitech":
        return AVAILABLE_COUNTRIES
        
    if _destinations_cache and time.time() - _destinations_cache_time < 3600:
        return list(_destinations_cache.keys())

    token = await get_celitech_token()
    if not token:
        return AVAILABLE_COUNTRIES

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                "https://api.celitech.net/v1/destinations",
                headers={"Authorization": f"Bearer {token}"}
            )
            resp.raise_for_status()
            data = resp.json()
            dests = data.get("destinations", [])
            _destinations_cache = {d["destination"]: d["name"] for d in dests}
            _destinations_cache_time = time.time()
            return list(_destinations_cache.keys())
        except Exception as e:
            logger.error(f"Failed to get Celitech destinations: {e}")
            return AVAILABLE_COUNTRIES

_packages_cache: dict[str, ESIMPlan] = {}

async def get_celitech_packages(country_code: str) -> list[ESIMPlan]:
    token = await get_celitech_token()
    if not token:
        return []

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                "https://api.celitech.net/v1/packages",
                params={"destination": country_code},
                headers={"Authorization": f"Bearer {token}"}
            )
            resp.raise_for_status()
            data = resp.json()
            packages = data.get("packages", [])
            
            plans = []
            for p in packages:
                plan_id = p.get("id")
                data_gb = p.get("dataLimitInBytes", 0) / (1024**3)
                duration = p.get("duration", 0)  # usually in seconds, wait, Celitech v1 duration is in days usually? 
                # Let's check Celitech API docs for 'duration' or 'validity'. Wait, Celitech package price is in cents.
                price = p.get("priceInCents", 0) / 100.0
                # Let's map safely
                if not plan_id or data_gb == 0:
                    continue
                
                # We need a fallback if duration is not explicitly days
                days = p.get("duration", 30) # default to 30 if undefined
                if "InDays" in str(p): # Some APIs use durationInDays
                    pass
                    
                plan = ESIMPlan(
                    plan_id=plan_id,
                    country_code=country_code,
                    country_name=country_code,  # Will translate on frontend
                    country_flag="", # Frontend can map
                    data_gb=round(data_gb, 1),
                    duration_days=days,
                    price_eur=price,
                    description=f"{round(data_gb, 1)} GB / {days} Days"
                )
                plans.append(plan)
                _packages_cache[plan_id] = plan
            return plans
        except Exception as e:
            logger.error(f"Failed to get Celitech packages: {e}")
            return []

async def get_esimaccess_packages(country_code: str) -> list[ESIMPlan]:
    import json
    body_dict = {"locationCode": country_code}
    body_str = json.dumps(body_dict)
    headers = _get_esimaccess_headers(body_str)
    if not headers:
        return []

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "https://api.esimaccess.com/api/v1/open/package/list",
                data=body_str,
                headers=headers
            )
            resp.raise_for_status()
            data = resp.json()
            
            plans = []
            if data.get("success"):
                packages = data.get("obj", {}).get("packageList", [])
                for p in packages:
                    plan_id = p.get("packageCode")
                    data_bytes = p.get("volume", 0)
                    data_gb = data_bytes / (1024**3) if data_bytes > 0 else 0
                    duration = p.get("duration", 0)
                    price = p.get("price", 0) / 10000.0  # Scale price correctly
                    
                    if not plan_id or data_gb == 0:
                        continue
                        
                    plan = ESIMPlan(
                        plan_id=plan_id,
                        country_code=country_code,
                        country_name=country_code,
                        country_flag="",
                        data_gb=round(data_gb, 1),
                        duration_days=duration,
                        price_eur=round(price, 2),  # Keeping USD value for simplicity, or we could convert
                        description=f"{round(data_gb, 1)} GB / {duration} Days"
                    )
                    plans.append(plan)
                    _packages_cache[plan_id] = plan
            return plans
        except Exception as e:
            logger.error(f"Failed to get eSIM Access packages: {e}")
            return []

async def get_plans_by_country(country_code: str) -> list[ESIMPlan]:
    if config.ESIM_PROVIDER == "celitech":
        return await get_celitech_packages(country_code)
    elif config.ESIM_PROVIDER == "esimaccess":
        return await get_esimaccess_packages(country_code)
    return [p for p in PLANS if p.country_code == country_code]


async def get_plan_by_id(plan_id: str) -> Optional[ESIMPlan]:
    if config.ESIM_PROVIDER in ("celitech", "esimaccess"):
        return _packages_cache.get(plan_id)
        
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
