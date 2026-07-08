from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Integer, Boolean, DateTime, ForeignKey, Text, func
from datetime import datetime
from typing import Optional, List

from config import config

engine = create_async_engine(config.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    full_name: Mapped[str] = mapped_column(String(128))
    language: Mapped[str] = mapped_column(String(8), default="ru")
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    referral_code: Mapped[str] = mapped_column(String(16), unique=True)
    referred_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    plan_id: Mapped[str] = mapped_column(String(64))
    country_code: Mapped[str] = mapped_column(String(8))
    country_name: Mapped[str] = mapped_column(String(64))
    data_gb: Mapped[float] = mapped_column(Float)
    duration_days: Mapped[int] = mapped_column(Integer)
    price_eur: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(32), default="pending")  # pending|paid|activated|failed
    payment_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    esim_iccid: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    esim_qr_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # base64 or URL
    esim_activation_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    activated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="orders")


class ReferralBonus(Base):
    __tablename__ = "referral_bonuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referrer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    referred_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    bonus_amount: Mapped[float] = mapped_column(Float)
    paid: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
