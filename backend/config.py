import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "esim_advance_bot")
    ADMIN_IDS: list = None
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    # OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    APPLE_CLIENT_ID: str = os.getenv("APPLE_CLIENT_ID", "")
    APPLE_TEAM_ID: str = os.getenv("APPLE_TEAM_ID", "")
    APPLE_KEY_ID: str = os.getenv("APPLE_KEY_ID", "")
    APPLE_PRIVATE_KEY: str = os.getenv("APPLE_PRIVATE_KEY", "").replace('\\n', '\n')
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-session-key")

    # eSIM Provider API (подключить позже — Airalo / eSIM Go)
    ESIM_PROVIDER: str = os.getenv("ESIM_PROVIDER", "mock")  # "mock" | "airalo" | "esimgo"
    ESIM_API_KEY: str = os.getenv("ESIM_API_KEY", "")
    ESIM_API_URL: str = os.getenv("ESIM_API_URL", "")

    # Referral settings
    REFERRAL_BONUS_EUR: float = float(os.getenv("REFERRAL_BONUS_EUR", "2.0"))

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://esim_user:esim_pass@db:5432/esim_db")

    def __post_init__(self):
        if self.ADMIN_IDS is None:
            admin_str = os.getenv("ADMIN_IDS", "")
            self.ADMIN_IDS = [int(x) for x in admin_str.split(",") if x.strip()]

        if not self.SECRET_KEY or self.SECRET_KEY == "your-super-secret-session-key":
            secret_path = os.getenv("KEYS_DIR", "/app/keys") + "/session_secret.txt"
            if os.path.exists(secret_path):
                with open(secret_path, "r") as f:
                    self.SECRET_KEY = f.read().strip()


config = Config()
