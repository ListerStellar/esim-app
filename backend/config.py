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
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-session-key")

    # eSIM Provider API
    ESIM_PROVIDER: str = os.getenv("ESIM_PROVIDER", "mock")  # "mock" | "airalo" | "esimgo" | "celitech"
    ESIM_API_KEY: str = os.getenv("ESIM_API_KEY", "")
    ESIM_API_URL: str = os.getenv("ESIM_API_URL", "")
    CELITECH_CLIENT_ID: str = os.getenv("CELITECH_CLIENT_ID", "")
    CELITECH_CLIENT_SECRET: str = os.getenv("CELITECH_CLIENT_SECRET", "")
    ESIMACCESS_ACCESS_CODE: str = os.getenv("ESIMACCESS_ACCESS_CODE", "")
    ESIMACCESS_SECRET_KEY: str = os.getenv("ESIMACCESS_SECRET_KEY", "")

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
