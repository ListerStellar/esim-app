import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "esim_advance_bot")
    ADMIN_IDS: list = None
    
    # Backend connection
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://backend:8000")
    INTERNAL_API_TOKEN: str = os.getenv("INTERNAL_API_TOKEN", "super-secret-internal-token")

    # Settings
    REFERRAL_BONUS_EUR: float = float(os.getenv("REFERRAL_BONUS_EUR", "2.0"))

    # Webhook
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "https://your.ngrok-free.app")
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook/bot")
    WEBAPP_HOST: str = os.getenv("WEBAPP_HOST", "0.0.0.0")
    WEBAPP_PORT: int = int(os.getenv("WEBAPP_PORT", "8080"))

    def __post_init__(self):
        if self.ADMIN_IDS is None:
            admin_str = os.getenv("ADMIN_IDS", "")
            self.ADMIN_IDS = [int(x) for x in admin_str.split(",") if x.strip()]


config = Config()
