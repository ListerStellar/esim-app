from typing import Dict, Any

# Languages: ru, en, cs, uk
TEXTS: Dict[str, Dict[str, Any]] = {
    "ru": {
        # Reply Keyboard Buttons
        "btn_buy": "🌍 Купить eSIM",
        "btn_profile": "👤 Профиль",
        "btn_orders": "📦 Мои заказы",
        "btn_referral": "🎁 Реферальная программа",
        "btn_install": "❓ Как установить eSIM",
        "btn_support": "💬 Поддержка",

        # Inline Keyboard Buttons
        "btn_lang": "🌐 Сменить язык",
        "btn_close": "❌ Закрыть",
        "btn_back_countries": "◀️ Назад к странам",
        "btn_pay_card": "💳 Оплатить картой",
        "btn_pay_balance": "💰 Оплатить с баланса",
        "btn_cancel": "❌ Отмена",
        "btn_go_pay": "💳 Перейти к оплате",
        "btn_i_paid": "✅ Я оплатил",
        "btn_share": "📤 Поделиться ссылкой",
        
        # Profile & Orders
        "profile_title": "👤 <b>Профиль</b>",
        "profile_id": "🆔 ID:",
        "profile_name": "👤 Имя:",
        "profile_balance": "💰 Баланс:",
        "profile_orders": "📦 Заказов:",
        "profile_lang": "🌐 Язык:",
        "profile_ref": "🔑 Реферальный код:",
        "profile_not_found": "Пользователь не найден. Напиши /start",
        "orders_empty": "📦 У тебя пока нет заказов.\n\nНажми <b>🌍 Купить eSIM</b> для начала!",
        "orders_title": "📦 <b>История заказов</b>",
        "order_status_pending": "⏳",
        "order_status_paid": "💳",
        "order_status_activated": "✅",
        "order_status_failed": "❌",
        
        # Order / Payment Handlers
        "payment_success": "✅ Оплата прошла успешно! Высылаем eSIM...",
        "payment_wait": "⏳ Оплата ещё не получена. Подождите несколько секунд и попробуйте снова.",
        "test_mode": "🧪 <b>Тестовый режим</b>\n\nСимулируем успешную оплату заказа #{order_id}...",
        "payment_invoice": "💳 <b>Оплата заказа #{order_id}</b>\n\nСумма: <b>{price}€</b>\n\nНажми кнопку ниже для перехода к оплате.\nПосле оплаты нажми «Я оплатил».",
        "payment_processing": "⏳ Обрабатываем платеж и выпускаем eSIM...",
        "payment_error": "❌ Ошибка:",
        "plan_not_found": "Тариф не найден",
        "user_not_found": "Пользователь не найден",
        "insufficient_funds": "Недостаточно средств. Баланс: {balance}€, нужно {price}€",
        "esim_activation_error": "Ошибка активации eSIM",
        "esim_activation_error_test": "Ошибка активации eSIM в тестовом режиме",
        "payment_system_error": "Ошибка платежной системы",
        "order_not_found": "Заказ не найден",
        "esim_already_activated": "eSIM уже активирован и отправлен!",
        "order_cancelled": "❌ Заказ отменён. Деньги не были списаны.",
        
        "admin_panel": "🔧 <b>Админ-панель</b>\n\n👥 Пользователей: <b>{total_users}</b>\n📦 Заказов всего: <b>{total_orders}</b>\n✅ Оплаченных: <b>{paid_orders}</b>\n💰 Выручка: <b>{revenue}€</b>\n\n<b>Команды:</b>\n/stats — статистика\n/addbalance [user_id] [amount] — пополнить баланс\n/broadcast [text] — рассылка (скоро)",
        "admin_stats": "📊 Пользователей: {total_users}\n📦 Заказов: {total_orders}\n✅ Оплачено: {paid_orders}\n💰 Выручка: {revenue}€",
        "admin_addbalance_usage": "Использование: /addbalance [telegram_id] [сумма]",
        "admin_invalid_format": "Неверный формат",
        "admin_user_not_found": "Пользователь не найден",
        "admin_balance_added": "✅ Пользователю {name} начислено {amount}€",
        
        # Catalog Handlers
        "choose_country": "🌍 <b>Выбери страну</b>\n\nВ какой стране нужен интернет?",
        "choose_plan": "📦 <b>Тарифы для {country}</b>\n\nВыбери подходящий пакет:",
        
        # Start & General
        "welcome": (
            "👋 Добро пожаловать в <b>eSIM Store</b>!\n\n"
            "🌍 Мобильный интернет в 50+ странах\n"
            "⚡️ Мгновенная активация — без очередей\n"
            "💰 Дешевле местных операторов до 3 раз\n\n"
            "Выбери язык / Choose language:"
        ),
        "main_menu": "🏠 <b>Главное меню</b>\n\nЧто хочешь сделать?",
        "lang_set": "✅ Язык выбран!",
        
        # Referral
        "ref_title": (
            "🎁 <b>Реферальная программа</b>\n\n"
            "Приглашай друзей и получай <b>{bonus}€</b> "
            "на баланс за каждого, кто сделает первый заказ!\n\n"
            "👥 Приглашено: <b>{count}</b> человек\n"
            "💰 Заработано: <b>{earned}€</b>\n\n"
            "🔗 Твоя ссылка:\n<code>{link}</code>\n\n"
            "Нажми «Поделиться» чтобы отправить ссылку друзьям 👇"
        ),
        "ref_share": "Советую eSIM Store — дешёвый мобильный интернет в 50+ странах!\nАктивация мгновенная, всё через Telegram.\n{link}",
        
        # eSIM strings
        "esim_ready": "🎉 <b>Ваш eSIM готов!</b>",
        "esim_ready_2": "✅ <b>Ваша eSIM #{order_id}</b>",
        "country": "🌍 Страна:",
        "data_gb": "📶 Данные:",
        "duration": "📅 Срок:",
        "how_to_install_short": (
            "📱 <b>Как установить:</b>\n"
            "1. Откройте Настройки → Сотовая связь → Добавить eSIM\n"
            "2. Выберите «Сканировать QR-код» и отсканируйте код выше\n"
            "   — или введите код активации вручную:\n\n"
            "<code>{activation_code}</code>\n\n"
            "⚠️ eSIM активируется при первом использовании.\n"
            "📋 Заказ #{order_id} | ICCID: <code>{iccid}</code>"
        ),
        "qr_scan_text": (
            "📱 <b>ICCID:</b> <code>{iccid}</code>\n"
            "🔑 <b>Код активации:</b>\n<code>{activation_code}</code>\n\n"
            "Отсканируйте QR-код выше камерой телефона или введите код активации вручную."
        ),
        "how_to_text": (
            "📱 <b>Как установить eSIM</b>\n\n"
            "<b>iPhone (iOS 12.1+):</b>\n"
            "1. Настройки → Сотовая связь\n"
            "2. Добавить сотовый план\n"
            "3. Сканируй QR-код\n\n"
            "<b>Android:</b>\n"
            "1. Настройки → Подключения → SIM-менеджер\n"
            "2. Добавить тарифный план / eSIM\n"
            "3. Сканируй QR-код\n\n"
            "<b>⚠️ Важно:</b>\n"
            "• Твой телефон должен поддерживать eSIM\n"
            "• Разблокирован от оператора (unlocked)\n"
            "• Нужен Wi-Fi или мобильный интернет для активации\n\n"
            "❓ Остались вопросы? Напиши в поддержку."
        ),
        "support_text": (
            "💬 <b>Поддержка</b>\n\n"
            "Работаем 9:00–21:00 (CET)\n"
            "Ответ обычно в течение 30 минут.\n\n"
        ),
    },
    "en": {
        "btn_buy": "🌍 Buy eSIM",
        "btn_profile": "👤 Profile",
        "btn_orders": "📦 My Orders",
        "btn_referral": "🎁 Referral Program",
        "btn_install": "❓ How to Install",
        "btn_support": "💬 Support",

        "btn_lang": "🌐 Change Language",
        "btn_close": "❌ Close",
        "btn_back_countries": "◀️ Back to Countries",
        "btn_pay_card": "💳 Pay with Card",
        "btn_pay_balance": "💰 Pay with Balance",
        "btn_cancel": "❌ Cancel",
        "btn_go_pay": "💳 Go to Payment",
        "btn_i_paid": "✅ I Paid",
        "btn_share": "📤 Share Link",
        
        "profile_title": "👤 <b>Profile</b>",
        "profile_id": "🆔 ID:",
        "profile_name": "👤 Name:",
        "profile_balance": "💰 Balance:",
        "profile_orders": "📦 Orders:",
        "profile_lang": "🌐 Language:",
        "profile_ref": "🔑 Referral Code:",
        "profile_not_found": "User not found. Please send /start",
        "orders_empty": "📦 You don't have any orders yet.\n\nClick <b>🌍 Buy eSIM</b> to start!",
        "orders_title": "📦 <b>Order History</b>",
        "order_status_pending": "⏳",
        "order_status_paid": "💳",
        "order_status_activated": "✅",
        "order_status_failed": "❌",

        "payment_success": "✅ Payment successful! Sending your eSIM...",
        "payment_wait": "⏳ Payment not received yet. Please wait a few seconds and try again.",
        "test_mode": "🧪 <b>Test Mode</b>\n\nSimulating successful payment for order #{order_id}...",
        "payment_invoice": "💳 <b>Order Payment #{order_id}</b>\n\nAmount: <b>{price}€</b>\n\nClick the button below to pay.\nAfter payment, click «I Paid».",
        "payment_processing": "⏳ Processing payment and generating eSIM...",
        "payment_error": "❌ Error:",
        "plan_not_found": "Plan not found",
        "user_not_found": "User not found",
        "insufficient_funds": "Insufficient funds. Balance: {balance}€, required {price}€",
        "esim_activation_error": "eSIM activation error",
        "esim_activation_error_test": "eSIM activation error in test mode",
        "payment_system_error": "Payment system error",
        "order_not_found": "Order not found",
        "esim_already_activated": "eSIM is already activated and sent!",
        "order_cancelled": "❌ Order cancelled. You were not charged.",

        "admin_panel": "🔧 <b>Admin Panel</b>\n\n👥 Users: <b>{total_users}</b>\n📦 Total Orders: <b>{total_orders}</b>\n✅ Paid: <b>{paid_orders}</b>\n💰 Revenue: <b>{revenue}€</b>\n\n<b>Commands:</b>\n/stats — statistics\n/addbalance [user_id] [amount] — add balance\n/broadcast [text] — broadcast (soon)",
        "admin_stats": "📊 Users: {total_users}\n📦 Orders: {total_orders}\n✅ Paid: {paid_orders}\n💰 Revenue: {revenue}€",
        "admin_addbalance_usage": "Usage: /addbalance [telegram_id] [amount]",
        "admin_invalid_format": "Invalid format",
        "admin_user_not_found": "User not found",
        "admin_balance_added": "✅ Added {amount}€ to user {name}",

        "choose_country": "🌍 <b>Choose Country</b>\n\nWhere do you need internet?",
        "choose_plan": "📦 <b>Plans for {country}</b>\n\nChoose a suitable plan:",

        "welcome": (
            "👋 Welcome to <b>eSIM Store</b>!\n\n"
            "🌍 Mobile internet in 50+ countries\n"
            "⚡️ Instant activation — no queues\n"
            "💰 Up to 3x cheaper than local carriers\n\n"
            "Choose language:"
        ),
        "main_menu": "🏠 <b>Main Menu</b>\n\nWhat would you like to do?",
        "lang_set": "✅ Language set!",

        "ref_title": (
            "🎁 <b>Referral Program</b>\n\n"
            "Invite friends and get <b>{bonus}€</b> "
            "to your balance for everyone who makes their first order!\n\n"
            "👥 Invited: <b>{count}</b> people\n"
            "💰 Earned: <b>{earned}€</b>\n\n"
            "🔗 Your link:\n<code>{link}</code>\n\n"
            "Click «Share» to send the link to friends 👇"
        ),
        "ref_share": "I recommend eSIM Store — cheap mobile internet in 50+ countries!\nInstant activation directly in Telegram.\n{link}",

        "esim_ready": "🎉 <b>Your eSIM is ready!</b>",
        "esim_ready_2": "✅ <b>Your eSIM #{order_id}</b>",
        "country": "🌍 Country:",
        "data_gb": "📶 Data:",
        "duration": "📅 Duration:",
        "how_to_install_short": (
            "📱 <b>How to install:</b>\n"
            "1. Open Settings → Cellular → Add eSIM\n"
            "2. Select «Scan QR Code» and scan the code above\n"
            "   — or enter activation code manually:\n\n"
            "<code>{activation_code}</code>\n\n"
            "⚠️ eSIM activates upon first usage.\n"
            "📋 Order #{order_id} | ICCID: <code>{iccid}</code>"
        ),
        "qr_scan_text": (
            "📱 <b>ICCID:</b> <code>{iccid}</code>\n"
            "🔑 <b>Activation Code:</b>\n<code>{activation_code}</code>\n\n"
            "Scan the QR code above with your phone camera or enter the activation code manually."
        ),
        "how_to_text": (
            "📱 <b>How to install eSIM</b>\n\n"
            "<b>iPhone (iOS 12.1+):</b>\n"
            "1. Settings → Cellular\n"
            "2. Add Cellular Plan\n"
            "3. Scan QR Code\n\n"
            "<b>Android:</b>\n"
            "1. Settings → Connections → SIM Manager\n"
            "2. Add Mobile Plan / eSIM\n"
            "3. Scan QR Code\n\n"
            "<b>⚠️ Important:</b>\n"
            "• Your phone must support eSIM\n"
            "• Device must be unlocked from carrier\n"
            "• Wi-Fi or mobile data is required for activation\n\n"
            "❓ Have questions? Contact support."
        ),
        "support_text": (
            "💬 <b>Support</b>\n\n"
            "Working hours: 9:00–21:00 (CET)\n"
            "Average response time is 30 minutes.\n\n"
        ),
    },
    "cs": {
        "btn_buy": "🌍 Koupit eSIM",
        "btn_profile": "👤 Profil",
        "btn_orders": "📦 Moje objednávky",
        "btn_referral": "🎁 Partnerský program",
        "btn_install": "❓ Jak nainstalovat",
        "btn_support": "💬 Podpora",

        "btn_lang": "🌐 Změnit jazyk",
        "btn_close": "❌ Zavřít",
        "btn_back_countries": "◀️ Zpět na země",
        "btn_pay_card": "💳 Zaplatit kartou",
        "btn_pay_balance": "💰 Zaplatit ze zůstatku",
        "btn_cancel": "❌ Zrušit",
        "btn_go_pay": "💳 Přejít k platbě",
        "btn_i_paid": "✅ Zaplatil(a) jsem",
        "btn_share": "📤 Sdílet odkaz",
        
        "profile_title": "👤 <b>Profil</b>",
        "profile_id": "🆔 ID:",
        "profile_name": "👤 Jméno:",
        "profile_balance": "💰 Zůstatek:",
        "profile_orders": "📦 Objednávky:",
        "profile_lang": "🌐 Jazyk:",
        "profile_ref": "🔑 Doporučující kód:",
        "profile_not_found": "Uživatel nenalezen. Napište /start",
        "orders_empty": "📦 Zatím nemáte žádné objednávky.\n\nKlikněte na <b>🌍 Koupit eSIM</b> a začněte!",
        "orders_title": "📦 <b>Historie objednávek</b>",
        "order_status_pending": "⏳",
        "order_status_paid": "💳",
        "order_status_activated": "✅",
        "order_status_failed": "❌",

        "payment_success": "✅ Platba byla úspěšná! Odesíláme eSIM...",
        "payment_wait": "⏳ Platba zatím nebyla přijata. Počkejte prosím několik sekund a zkuste to znovu.",
        "test_mode": "🧪 <b>Testovací režim</b>\n\nSimulujeme úspěšnou platbu objednávky #{order_id}...",
        "payment_invoice": "💳 <b>Platba objednávky #{order_id}</b>\n\nČástka: <b>{price}€</b>\n\nKliknutím na tlačítko níže přejděte k platbě.\nPo zaplacení klikněte na «Zaplatil(a) jsem».",
        "payment_processing": "⏳ Zpracováváme platbu a generujeme eSIM...",
        "payment_error": "❌ Chyba:",
        "plan_not_found": "Tarif nenalezen",
        "user_not_found": "Uživatel nenalezen",
        "insufficient_funds": "Nedostatek prostředků. Zůstatek: {balance}€, je potřeba {price}€",
        "esim_activation_error": "Chyba aktivace eSIM",
        "esim_activation_error_test": "Chyba aktivace eSIM v testovacím režimu",
        "payment_system_error": "Chyba platebního systému",
        "order_not_found": "Objednávka nenalezena",
        "esim_already_activated": "eSIM již byla aktivována a odeslána!",
        "order_cancelled": "❌ Objednávka byla zrušena. Peníze nebyly odečteny.",

        "admin_panel": "🔧 <b>Admin panel</b>\n\n👥 Uživatelů: <b>{total_users}</b>\n📦 Celkem objednávek: <b>{total_orders}</b>\n✅ Zaplaceno: <b>{paid_orders}</b>\n💰 Tržby: <b>{revenue}€</b>\n\n<b>Příkazy:</b>\n/stats — statistika\n/addbalance [user_id] [amount] — dobít kredit\n/broadcast [text] — rozeslat zprávu (brzy)",
        "admin_stats": "📊 Uživatelů: {total_users}\n📦 Objednávek: {total_orders}\n✅ Zaplaceno: {paid_orders}\n💰 Tržby: {revenue}€",
        "admin_addbalance_usage": "Použití: /addbalance [telegram_id] [částka]",
        "admin_invalid_format": "Neplatný formát",
        "admin_user_not_found": "Uživatel nenalezen",
        "admin_balance_added": "✅ Uživateli {name} bylo připsáno {amount}€",

        "choose_country": "🌍 <b>Vyberte zemi</b>\n\nKde potřebujete internet?",
        "choose_plan": "📦 <b>Tarify pro {country}</b>\n\nVyberte vhodný tarif:",

        "welcome": (
            "👋 Vítejte v <b>eSIM Store</b>!\n\n"
            "🌍 Mobilní internet ve 50+ zemích\n"
            "⚡️ Okamžitá aktivace\n"
            "💰 Levnější než místní operátoři\n\n"
            "Vyberte jazyk / Choose language:"
        ),
        "main_menu": "🏠 <b>Hlavní menu</b>\n\nCo chcete udělat?",
        "lang_set": "✅ Jazyk byl nastaven!",

        "ref_title": (
            "🎁 <b>Partnerský program</b>\n\n"
            "Pozvěte přátele a získejte <b>{bonus}€</b> "
            "na svůj zůstatek za každého, kdo udělá první objednávku!\n\n"
            "👥 Pozváno: <b>{count}</b> lidí\n"
            "💰 Vyděláno: <b>{earned}€</b>\n\n"
            "🔗 Váš odkaz:\n<code>{link}</code>\n\n"
            "Kliknutím na «Sdílet» odešlete odkaz přátelům 👇"
        ),
        "ref_share": "Doporučuji eSIM Store — levný mobilní internet ve 50+ zemích!\nOkamžitá aktivace přímo v Telegramu.\n{link}",

        "esim_ready": "🎉 <b>Vaše eSIM je připravena!</b>",
        "esim_ready_2": "✅ <b>Vaše eSIM #{order_id}</b>",
        "country": "🌍 Země:",
        "data_gb": "📶 Data:",
        "duration": "📅 Trvání:",
        "how_to_install_short": (
            "📱 <b>Jak nainstalovat:</b>\n"
            "1. Otevřete Nastavení → Mobilní data → Přidat eSIM\n"
            "2. Vyberte «Skenovat QR kód» a naskenujte kód výše\n"
            "   — nebo zadejte aktivační kód ručně:\n\n"
            "<code>{activation_code}</code>\n\n"
            "⚠️ eSIM se aktivuje při prvním použití.\n"
            "📋 Objednávka #{order_id} | ICCID: <code>{iccid}</code>"
        ),
        "qr_scan_text": (
            "📱 <b>ICCID:</b> <code>{iccid}</code>\n"
            "🔑 <b>Aktivační kód:</b>\n<code>{activation_code}</code>\n\n"
            "Naskenujte QR kód výše pomocí fotoaparátu telefonu nebo zadejte aktivační kód ručně."
        ),
        "how_to_text": (
            "📱 <b>Jak nainstalovat eSIM</b>\n\n"
            "<b>iPhone (iOS 12.1+):</b>\n"
            "1. Nastavení → Mobilní data\n"
            "2. Přidat mobilní tarif\n"
            "3. Skenovat QR kód\n\n"
            "<b>Android:</b>\n"
            "1. Nastavení → Připojení → Správce SIM\n"
            "2. Přidat mobilní tarif / eSIM\n"
            "3. Skenovat QR kód\n\n"
            "<b>⚠️ Důležité:</b>\n"
            "• Váš telefon musí podporovat eSIM\n"
            "• Zařízení nesmí být blokováno operátorem\n"
            "• K aktivaci je vyžadováno Wi-Fi nebo mobilní připojení\n\n"
            "❓ Máte dotazy? Napište podpoře."
        ),
        "support_text": (
            "💬 <b>Podpora</b>\n\n"
            "Pracovní doba: 9:00–21:00 (CET)\n"
            "Průměrná doba odezvy je 30 minut.\n\n"
        ),
    },
    "uk": {
        "btn_buy": "🌍 Купити eSIM",
        "btn_profile": "👤 Профіль",
        "btn_orders": "📦 Мої замовлення",
        "btn_referral": "🎁 Реферальна програма",
        "btn_install": "❓ Як встановити",
        "btn_support": "💬 Підтримка",

        "btn_lang": "🌐 Змінити мову",
        "btn_close": "❌ Закрити",
        "btn_back_countries": "◀️ Назад до країн",
        "btn_pay_card": "💳 Оплатити карткою",
        "btn_pay_balance": "💰 Оплатити з балансу",
        "btn_cancel": "❌ Скасувати",
        "btn_go_pay": "💳 Перейти до оплати",
        "btn_i_paid": "✅ Я оплатив",
        "btn_share": "📤 Поділитися посиланням",
        
        "profile_title": "👤 <b>Профіль</b>",
        "profile_id": "🆔 ID:",
        "profile_name": "👤 Ім'я:",
        "profile_balance": "💰 Баланс:",
        "profile_orders": "📦 Замовлень:",
        "profile_lang": "🌐 Мова:",
        "profile_ref": "🔑 Реферальний код:",
        "profile_not_found": "Користувача не знайдено. Напишіть /start",
        "orders_empty": "📦 У вас поки немає замовлень.\n\nНатисніть <b>🌍 Купити eSIM</b> для початку!",
        "orders_title": "📦 <b>Історія замовлень</b>",
        "order_status_pending": "⏳",
        "order_status_paid": "💳",
        "order_status_activated": "✅",
        "order_status_failed": "❌",

        "payment_success": "✅ Оплата пройшла успішно! Надсилаємо eSIM...",
        "payment_wait": "⏳ Оплата ще не отримана. Зачекайте кілька секунд і спробуйте знову.",
        "test_mode": "🧪 <b>Тестовий режим</b>\n\nСимулюємо успішну оплату замовлення #{order_id}...",
        "payment_invoice": "💳 <b>Оплата замовлення #{order_id}</b>\n\nСума: <b>{price}€</b>\n\nНатисніть кнопку нижче для переходу до оплати.\nПісля оплати натисніть «Я оплатив».",
        "payment_processing": "⏳ Обробляємо платіж та випускаємо eSIM...",
        "payment_error": "❌ Помилка:",
        "plan_not_found": "Тариф не знайдено",
        "user_not_found": "Користувача не знайдено",
        "insufficient_funds": "Недостатньо коштів. Баланс: {balance}€, потрібно {price}€",
        "esim_activation_error": "Помилка активації eSIM",
        "esim_activation_error_test": "Помилка активації eSIM в тестовому режимі",
        "payment_system_error": "Помилка платіжної системи",
        "order_not_found": "Замовлення не знайдено",
        "esim_already_activated": "eSIM вже активовано та відправлено!",
        "order_cancelled": "❌ Замовлення скасовано. Гроші не були зняті.",

        "admin_panel": "🔧 <b>Адмін-панель</b>\n\n👥 Користувачів: <b>{total_users}</b>\n📦 Всього замовлень: <b>{total_orders}</b>\n✅ Оплачених: <b>{paid_orders}</b>\n💰 Виручка: <b>{revenue}€</b>\n\n<b>Команди:</b>\n/stats — статистика\n/addbalance [user_id] [amount] — поповнити баланс\n/broadcast [text] — розсилка (незабаром)",
        "admin_stats": "📊 Користувачів: {total_users}\n📦 Замовлень: {total_orders}\n✅ Оплачено: {paid_orders}\n💰 Виручка: {revenue}€",
        "admin_addbalance_usage": "Використання: /addbalance [telegram_id] [сума]",
        "admin_invalid_format": "Невірний формат",
        "admin_user_not_found": "Користувача не знайдено",
        "admin_balance_added": "✅ Користувачу {name} нараховано {amount}€",

        "choose_country": "🌍 <b>Оберіть країну</b>\n\nВ якій країні потрібен інтернет?",
        "choose_plan": "📦 <b>Тарифи для {country}</b>\n\nОберіть відповідний пакет:",

        "welcome": (
            "👋 Ласкаво просимо до <b>eSIM Store</b>!\n\n"
            "🌍 Мобільний інтернет у 50+ країнах\n"
            "⚡️ Миттєва активація — без черг\n"
            "💰 Дешевше за місцевих операторів до 3 разів\n\n"
            "Виберіть мову / Choose language:"
        ),
        "main_menu": "🏠 <b>Головне меню</b>\n\nЩо хочете зробити?",
        "lang_set": "✅ Мову встановлено!",

        "ref_title": (
            "🎁 <b>Реферальна програма</b>\n\n"
            "Запрошуй друзів і отримуй <b>{bonus}€</b> "
            "на баланс за кожного, хто зробить перше замовлення!\n\n"
            "👥 Запрошено: <b>{count}</b> осіб\n"
            "💰 Зароблено: <b>{earned}€</b>\n\n"
            "🔗 Твоє посилання:\n<code>{link}</code>\n\n"
            "Натисни «Поділитися» щоб відправити посилання друзям 👇"
        ),
        "ref_share": "Раджу eSIM Store — дешевий мобільний інтернет у 50+ країнах!\nАктивація миттєва, все через Telegram.\n{link}",

        "esim_ready": "🎉 <b>Ваша eSIM готова!</b>",
        "esim_ready_2": "✅ <b>Ваша eSIM #{order_id}</b>",
        "country": "🌍 Країна:",
        "data_gb": "📶 Дані:",
        "duration": "📅 Строк:",
        "how_to_install_short": (
            "📱 <b>Як встановити:</b>\n"
            "1. Відкрийте Налаштування → Стільникові дані → Додати eSIM\n"
            "2. Виберіть «Сканувати QR-код» і відскануйте код вище\n"
            "   — або введіть код активації вручну:\n\n"
            "<code>{activation_code}</code>\n\n"
            "⚠️ eSIM активується під час першого використання.\n"
            "📋 Замовлення #{order_id} | ICCID: <code>{iccid}</code>"
        ),
        "qr_scan_text": (
            "📱 <b>ICCID:</b> <code>{iccid}</code>\n"
            "🔑 <b>Код активації:</b>\n<code>{activation_code}</code>\n\n"
            "Відскануйте QR-код вище камерою телефону або введіть код активації вручну."
        ),
        "how_to_text": (
            "📱 <b>Як встановити eSIM</b>\n\n"
            "<b>iPhone (iOS 12.1+):</b>\n"
            "1. Налаштування → Стільникові дані\n"
            "2. Додати стільниковий тариф\n"
            "3. Сканувати QR-код\n\n"
            "<b>Android:</b>\n"
            "1. Налаштування → Підключення → Диспетчер SIM\n"
            "2. Додати мобільний тариф / eSIM\n"
            "3. Сканувати QR-код\n\n"
            "<b>⚠️ Важливо:</b>\n"
            "• Твій телефон повинен підтримувати eSIM\n"
            "• Розблокований від оператора (unlocked)\n"
            "• Потрібен Wi-Fi або мобільний інтернет для активації\n\n"
            "❓ Залишилися питання? Напиши в підтримку."
        ),
        "support_text": (
            "💬 <b>Підтримка</b>\n\n"
            "Працюємо 9:00–21:00 (CET)\n"
            "Відповідь зазвичай протягом 30 хвилин.\n\n"
        ),
    },
}

# Helper lists for aiogram message filters
MENU_BTN_BUY = [TEXTS[l]["btn_buy"] for l in TEXTS]
MENU_BTN_PROFILE = [TEXTS[l]["btn_profile"] for l in TEXTS]
MENU_BTN_ORDERS = [TEXTS[l]["btn_orders"] for l in TEXTS]
MENU_BTN_REFERRAL = [TEXTS[l]["btn_referral"] for l in TEXTS]
MENU_BTN_INSTALL = [TEXTS[l]["btn_install"] for l in TEXTS]
MENU_BTN_SUPPORT = [TEXTS[l]["btn_support"] for l in TEXTS]


def get_text(lang: str, key: str, **kwargs) -> str:
    """Retrieve localized string. Fallback to 'ru' if missing."""
    lang_dict = TEXTS.get(lang, TEXTS["ru"])
    text = lang_dict.get(key)
    
    if text is None:
        # Fallback to RU
        text = TEXTS["ru"].get(key, key)
        
    if kwargs:
        return text.format(**kwargs)
    return text

def get_error_text(lang: str, backend_error: str) -> str:
    if backend_error.startswith("insufficient_funds|"):
        try:
            _, bal, req = backend_error.split("|")
            return get_text(lang, "insufficient_funds", balance=bal, price=req)
        except ValueError:
            pass
    return get_text(lang, backend_error)
