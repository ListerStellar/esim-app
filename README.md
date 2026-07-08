# eSIM Store Bot 🌍

Telegram-бот для продажи eSIM. Работает с Airalo, eSIM Go или в тестовом режиме.

## Что умеет бот

- 🌍 Каталог тарифов по странам (Чехия, Европа, Германия, США и др.)
- 💳 Оплата через Stripe (карта) или с внутреннего баланса
- 📱 Мгновенная доставка QR-кода eSIM прямо в чат
- 👤 Личный кабинет: баланс, история заказов
- 🎁 Реферальная программа (+2€ за каждого друга)
- 🌐 Мультиязычный: RU / CS / EN / UK
- 🔧 Админ-панель: статистика, начисление баланса

---

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
cp .env.example .env
# Открой .env и заполни переменные
```

**Обязательно:**
- `BOT_TOKEN` — получи у [@BotFather](https://t.me/BotFather)
- `ADMIN_IDS` — свой Telegram ID (узнай у [@userinfobot](https://t.me/userinfobot))

**Опционально для полноценной работы:**
- `STRIPE_SECRET_KEY` — из [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
- `ESIM_PROVIDER` + `ESIM_API_KEY` — от выбранного поставщика

### 3. Запуск

```bash
python bot.py
```

Бот запустится в тестовом режиме (`ESIM_PROVIDER=mock`) — можно тестировать весь флоу без реальных API.

---

## Подключение eSIM поставщика

### Airalo Partners
1. Зарегистрируйся на [partners.airalo.com](https://partners.airalo.com)
2. Получи API ключ
3. В `.env` установи:
   ```
   ESIM_PROVIDER=airalo
   ESIM_API_KEY=your_key
   ESIM_API_URL=https://sandbox-partners-api.airalo.com
   ```
4. После тестирования смени URL на `https://partners-api.airalo.com`

### eSIM Go
1. Зарегистрируйся на [esim-go.com](https://www.esim-go.com)
2. В `.env` установи:
   ```
   ESIM_PROVIDER=esimgo
   ESIM_API_KEY=your_key
   ESIM_API_URL=https://api.esim-go.com
   ```

---

## Структура проекта

```
esim_bot/
├── bot.py                  # Точка входа
├── config.py               # Конфигурация из .env
├── requirements.txt
├── .env.example
├── database/
│   ├── db.py               # SQLAlchemy модели
│   └── crud.py             # Операции с БД
├── handlers/
│   ├── start.py            # /start, выбор языка
│   ├── catalog.py          # Страны и тарифы
│   ├── order.py            # Оплата и доставка eSIM
│   ├── profile.py          # Профиль, заказы, инструкция
│   ├── referral.py         # Реферальная программа
│   └── admin.py            # Админ-команды
├── keyboards/
│   └── kb.py               # Все клавиатуры
└── services/
    ├── esim_provider.py    # Логика активации eSIM
    └── payment.py          # Stripe интеграция
```

---

## Деплой на сервер

### Бесплатные варианты для старта:
- **Railway** — [railway.app](https://railway.app) — $5/мес или бесплатный tier
- **Render** — [render.com](https://render.com) — есть бесплатный план
- **VPS** — любой (DigitalOcean, Hetzner от €4/мес)

### Запуск через systemd (VPS):

```ini
[Unit]
Description=eSIM Telegram Bot
After=network.target

[Service]
WorkingDirectory=/path/to/esim_bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
EnvironmentFile=/path/to/esim_bot/.env

[Install]
WantedBy=multi-user.target
```

---

## Добавить новые страны/тарифы

В файле `services/esim_provider.py` найди список `PLANS` и добавь новые тарифы:

```python
ESIMPlan("hu_3gb_14d", "HU", "Венгрия 🇭🇺", "🇭🇺", 3, 14, 4.9, "3 ГБ / 14 дней"),
```

---

## Webhook для Stripe (production)

Для автоматического подтверждения оплаты нужен HTTP-сервер (FastAPI/aiohttp).
Webhook обрабатывает событие `checkout.session.completed` и вызывает `deliver_esim()`.
Это следующий шаг после базового MVP.
