import httpx
import os
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def make_obj(d: Any) -> Any:
    if isinstance(d, dict):
        return DotDict({k: make_obj(v) for k, v in d.items()})
    if isinstance(d, list):
        return [make_obj(i) for i in d]
    return d

from config import config

class BackendClient:
    def __init__(self):
        self.base_url = config.BACKEND_URL
        self.token = config.INTERNAL_API_TOKEN
        
    def _headers(self):
        return {"X-Internal-Token": self.token}
        
    async def get_or_create_user(self, telegram_id: int, username: Optional[str], full_name: str, referral_code_used: Optional[str] = None):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/api/internal/users",
                json={"telegram_id": telegram_id, "username": username, "full_name": full_name, "referral_code_used": referral_code_used},
                headers=self._headers()
            )
            resp.raise_for_status()
            return make_obj(resp.json())
            
    async def get_user_by_telegram_id(self, telegram_id: int):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/api/internal/users/{telegram_id}",
                headers=self._headers()
            )
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return make_obj(resp.json())

    async def set_user_language(self, telegram_id: int, language: str):
        async with httpx.AsyncClient() as client:
            resp = await client.patch(
                f"{self.base_url}/api/internal/users/{telegram_id}/language",
                json={"language": language},
                headers=self._headers()
            )
            resp.raise_for_status()
            return make_obj(resp.json())

    async def update_user_balance(self, telegram_id: int, delta: float):
        async with httpx.AsyncClient() as client:
            resp = await client.patch(
                f"{self.base_url}/api/internal/users/{telegram_id}/balance",
                json={"delta": delta},
                headers=self._headers()
            )
            resp.raise_for_status()
            return make_obj(resp.json())

    async def get_user_orders(self, user_id: int):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/api/internal/users/{user_id}/orders",
                headers=self._headers()
            )
            resp.raise_for_status()
            return make_obj(resp.json())

    async def count_referrals(self, user_id: int):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/api/internal/users/{user_id}/referrals/count",
                headers=self._headers()
            )
            resp.raise_for_status()
            return resp.json()["count"]

    async def get_stats(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/api/internal/users/system/stats",
                headers=self._headers()
            )
            resp.raise_for_status()
            return resp.json()

    # --- ТРАНЗАКЦИОННЫЕ МЕТОДЫ ---

    async def buy_with_balance(self, telegram_id: int, plan_id: str):
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"{self.base_url}/api/internal/buy_with_balance",
                json={"telegram_id": telegram_id, "plan_id": plan_id},
                headers=self._headers()
            )
            resp.raise_for_status()
            return make_obj(resp.json())

    async def buy_with_stripe(self, telegram_id: int, plan_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/api/internal/buy_with_stripe",
                json={"telegram_id": telegram_id, "plan_id": plan_id},
                headers=self._headers()
            )
            resp.raise_for_status()
            return make_obj(resp.json())

    async def check_payment(self, order_id: int):
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{self.base_url}/api/internal/check_payment/{order_id}",
                headers=self._headers()
            )
            resp.raise_for_status()
            return make_obj(resp.json())

    async def get_countries(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/api/internal/catalog/countries", headers=self._headers())
            resp.raise_for_status()
            return make_obj(resp.json())

    async def get_plans_by_country(self, country_code: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/api/internal/catalog/plans/{country_code}", headers=self._headers())
            resp.raise_for_status()
            return make_obj(resp.json())

    async def get_plan_by_id(self, plan_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/api/internal/catalog/plan/{plan_id}", headers=self._headers())
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return make_obj(resp.json())

backend = BackendClient()
