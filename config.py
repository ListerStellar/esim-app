import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    ADMIN_IDS: list = None
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    # eSIM Provider API (подключить позже — Airalo / eSIM Go)
    ESIM_PROVIDER: str = os.getenv("ESIM_PROVIDER", "mock")  # "mock" | "airalo" | "esimgo"
    ESIM_API_KEY: str = os.getenv("ESIM_API_KEY", "")
    ESIM_API_URL: str = os.getenv("ESIM_API_URL", "")

    # Referral settings
    REFERRAL_BONUS_EUR: float = float(os.getenv("REFERRAL_BONUS_EUR", "2.0"))

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///esim_bot.db")

    def __post_init__(self):
        if self.ADMIN_IDS is None:
            admin_str = os.getenv("ADMIN_IDS", "")
            self.ADMIN_IDS = [int(x) for x in admin_str.split(",") if x.strip()]


config = Config()
