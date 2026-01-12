import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8550400671:AAHZdPJcWi_NtkurCHGxUgmRsQKMTu3826g"
CHANNEL_ID = -1003580316890
SITE_URL = "https://www.primefusioncars.com/"

# База данных водителей (для приветствия и автозаполнения)
DRIVERS = {
    5348697217: {
        "name": "Александр",
        "car_model": "Toyota Sienna Hybrid (WAV)",
        "car_number": "TLC-4827"
    },
    547004364: {
        "name": "Антон",
        "car_model": "Toyota Sienna Hybrid (WAV)",
        "car_number": "TLC-3912"
    }
}

ALLOWED_DRIVERS = set(DRIVERS.keys())

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== TEMP ==================
TEMP = {}

# ================== ТЕКСТЫ (ПОЛНЫЕ) ==================
TEXT = {
    "ru": {
        "choose_lang": "🌐 Выберите язык / Choose language",
        "work_info": (
            "🛠 *Обслуживание автомобиля*\n\n"
            "*Основной сервис и контакты:*\n\n"
            "🔧 *Игорь Электрик* — +1 (646) 420–7572\n"
            "📍 2029 E 24th St, Brooklyn, NY\n"
            "Мелкий ремонт и электрика.\n"
            "Работает у себя дома после 10:00, нужна запись.\n\n"
            "🚗 *K, R & S Auto Service*\n"
            "📍 2965 86th Street, Brooklyn, NY 11223\n"
            "📞 (718) 891–6626\n"
            "Без записи, лучше приезжать к открытию.\n"
            "Менеджеры Алекс и Гарри говорят по-русски.\n"
            "Без выходных.\n\n"
            "💰 *Оплата сервиса*\n"
            "Платить за сервис не нужно — это включено в аренду.\n"
            "Оплату счетов веду я.\n\n"
            "*Регулярное ТО:*\n"
            "• Замена масла каждые 7000 миль\n"
            "• Только full synthetic (Toyota / Mobil 1)\n"
            "  до 50k — 0W16\n"
            "  50k–150k — 0W20\n"
            "  150k+ — 5W30\n\n"
            "📸 *Фото ресита обязательно:*\n"
            "дата, номер авто, список работ, марка масла, цена.\n"
            "На СТО часто забывают писать марку масла — проверяйте.\n\n"
            "*Фильтры гибридной батареи:*\n"
            "• Менять раз в 6 месяцев\n"
            "• Фильтры выдаю я, в сервисе их нет\n"
            "*Дополнительно:*\n"
            "• Каждую 2-ю замену масла — фильтры салона и двигателя\n"
            "• Каждую замену масла — ротация колёс\n"
            "• Давление в шинах: 35 psi\n"
            "• Преждевременный износ шин — ответственность арендатора\n\n"
            "📸 После каждого ТО отправляйте в WhatsApp:\n"
            "• фото одометра\n\n"
            "*DMV-инспекция:*\n"
            "Проходит раз в 4 месяца — ответственность арендатора.\n"
            "Uber напоминает, Lyft — нет.\n"
            "В день инспекции — фото авто с 4 сторон.\n\n"
        ),
        "welcome_new": (
            "👋 Добро пожаловать в Prime Fusion!\n\n"
            "• Если вы *новый клиент* — нажмите 'Анкета' и заполните ее\n"
            "• Если хотите *разместить свои автомобили на сайте* — нажмите 'Контакты' и свяжитесь с нами\n"
            "• Для получения платной консультации - нажмите консультация"
        ),
        "welcome_allowed": "Вы в рабочем пространстве арендодатора.",
        "contacts": (
            "📞 Контакты:\n\n"
            "Telegram: @primefusion_admin\n"
            "Email: info@primefusioncars.com\n"
            "Администратор: @wateryz"
        ),
        "consult": (
            "💼 *Платная консультация*\n\n"
            "Стоимость: *$50 за один вопрос*\n\n"
            "Владелец компании делится *личным опытом*.\n"
            "Консультация *не является гарантией результата*."
        ),
        "consult_done": (
            "✅ Вопрос отправлен.\n"
            "Оплата и дальнейшие шаги — через администратора."
        ),
        "fail": "❌ К сожалению, на данный момент сервис вам не подходит.",
        "success": "✅ Вы подходите под условия.\n\nПерейдите на сайт.",
        "site": "🚗 Перейти на сайт",
        "work_intro": (
            "🧰 Рабочее меню\n\n"
            "📸 Фото обязательно.\n"
            "✍️ После фото можно оставить комментарий."
        ),
        "ask_car": "🚗 Введите номер автомобиля:",
        "ask_text": "✍️ Введите сообщение:",
        "ask_photo": "📸 Загрузите фото.",
        "ask_photo_dmv": "📸 Скиньте фото DMV-инспекции",
        "ask_photo_service": "📸 Загрузите фото ресита",
        "sent": "✅ Сообщение отправлено администрации.",
        "no_access": "⛔️ У вас нет доступа."
    },
    "en": {
        "choose_lang": "🌐 Choose language",
        "work_info": (
            "🛠 *Vehicle Maintenance*\n\n"
            "*Main service & contacts:*\n\n"
            "🔧 *Igor Electrician* — +1 (646) 420–7572\n"
            "📍 2029 E 24th St, Brooklyn, NY\n"
            "Minor repairs & electrical work.\n"
            "Works after 10:00 AM, appointment required.\n\n"
            "🚗 *K, R & S Auto Service*\n"
            "📍 2965 86th Street, Brooklyn, NY 11223\n"
            "📞 (718) 891–6626\n"
            "No appointment needed, arrive early.\n"
            "Managers Alex & Harry speak Russian.\n"
            "Open daily.\n\n"
            "💰 *Service payment*\n"
            "Service is included in rental price.\n"
            "I handle all payments.\n\n"
            "*Regular maintenance:*\n"
            "• Oil change every 7000 miles\n"
            "• Full synthetic only (Toyota / Mobil 1)\n"
            "  up to 50k — 0W16\n"
            "  50k–150k — 0W20\n"
            "  150k+ — 5W30\n\n"
            "📸 *Receipt photo required:*\n"
            "date, car number, work list, oil brand, price.\n\n"
            "*Hybrid battery filters:*\n"
            "• Replace every 6 months\n"
            "• Filters provided by me\n"
            "*Additional:*\n"
            "• Every 2nd oil change — cabin & engine filters\n"
            "• Every oil change — tire rotation\n"
            "• Tire pressure: 35 psi\n"
            "• Tire wear is tenant responsibility\n\n"
            "📸 After service send to WhatsApp:\n"
            "• odometer photo\n\n"
            "*DMV inspection:*\n"
            "Required every 4 months.\n"
            "Uber reminds, Lyft does not.\n"
            "Inspection day — photos from all 4 sides.\n\n"
        ),
        "welcome_new": (
            "👋 Welcome to Prime Fusion!\n\n"
            "• If you are a *new client* — tap 'Application' and fill out the form\n"
            "• If you want to *list your vehicles on our website* — tap 'Contacts' and get in touch with us\n"
            "• To receive a paid consultation — tap 'Consultation'"
        ),
        "welcome_allowed": "You are in the landlord workspace.",
        "contacts": (
            "📞 Contacts:\n\n"
            "Telegram: @primefusion_admin\n"
            "Email: info@primefusioncars.com\n"
            "Administrator: @wateryz"
        ),
        "consult": (
            "💼 *Paid consultation*\n\n"
            "$50 per question.\n"
            "Personal experience only.\n"
            "No guarantees."
        ),
        "consult_done": "✅ Question sent. Admin will contact you.",
        "fail": "❌ Unfortunately, the service is not available.",
        "success": "✅ You meet the requirements.\n\nVisit the website.",
        "site": "🚗 Go to website",
        "work_intro": (
            "🧰 Work menu\n\n"
            "📸 Photo is required.\n"
            "✍️ You can comment after photo."
        ),
        "ask_car": "🚗 Enter vehicle number:",
        "ask_text": "✍️ Enter message:",
        "ask_photo": "📸 Upload photo.",
        "ask_photo_dmv": "📸 Send DMV inspection photo",
        "ask_photo_service": "📸 Upload a photo of the receipt",
        "sent": "✅ Message sent.",
        "no_access": "⛔️ No access."
    }
}

# ================== КЛАВИАТУРЫ ==================
def lang_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang:en")
        ]
    ])

def menu_new_user_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Анкета" if lang=="ru" else "📝 Form", callback_data="menu:form")],
        [InlineKeyboardButton(text="📞 Контакты" if lang=="ru" else "📞 Contacts", callback_data="menu:contacts")],
        [InlineKeyboardButton(text="💼 Консультация" if lang=="ru" else "💼 Consultation", callback_data="menu:consult")]
    ])

def menu_allowed_user_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧰 Рабочее меню" if lang=="ru" else "🧰 Work menu", callback_data="menu:work")],
    ])

def work_menu_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🧾 DMV инспекция" if lang=="ru" else "🧾 DMV inspection",
            callback_data="work:dmv"
        )],
        [InlineKeyboardButton(
            text="🛠 Сервис и ремонт" if lang=="ru" else "🛠 Service",
            callback_data="work:service"
        )],
        [InlineKeyboardButton(
            text="ℹ️ Правила и инструкции" if lang=="ru" else "ℹ️ Rules and instructions",
            callback_data="work:info"
        )],
        [InlineKeyboardButton(
            text="📞 Связаться с администратором" if lang=="ru" else "📞 Contact admin",
            callback_data="work:admin"
        )],
    ])

def bottom_menu_kb(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 В главное меню" if lang == "ru" else "🔄 Main menu")]],
        resize_keyboard=True
    )

def yes_no_kb(step, lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да" if lang=="ru" else "✅ Yes", callback_data=f"{step}:yes"),
            InlineKeyboardButton(text="❌ Нет" if lang=="ru" else "❌ No", callback_data=f"{step}:no")
        ]
    ])

def site_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=TEXT[lang]["site"], web_app=WebAppInfo(url=SITE_URL))]
    ])

def get_lang(uid):
    return TEMP.get(uid, {}).get("lang", "ru")

# ================== ЛОГИКА ПРИВЕТСТВИЯ ==================
async def send_main_menu(message_or_callback, uid, lang):
    if uid in ALLOWED_DRIVERS:
        driver = DRIVERS[uid]
        welcome_text = (
            f"👋 Здравствуйте, *{driver['name']}*!\n"
            f"🚗 Ваш автомобиль: *{driver['car_model']}*\n"
            f"🔢 Номер: `{driver['car_number']}`\n\n"
            f"{TEXT[lang]['welcome_allowed']}"
            if lang == "ru" else
            f"👋 Hello, *{driver['name']}*!\n"
            f"🚗 Your car: *{driver['car_model']}*\n"
            f"🔢 Plate: `{driver['car_number']}`\n\n"
            f"{TEXT[lang]['welcome_allowed']}"
        )
        kb = menu_allowed_user_kb(lang)
    else:
        welcome_text = TEXT[lang]["welcome_new"]
        kb = menu_new_user_kb(lang)

    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(welcome_text, reply_markup=kb, parse_mode="Markdown")
    else:
        await message_or_callback.message.edit_text(welcome_text, reply_markup=kb, parse_mode="Markdown")

# ================== СТАРТ ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    uid = message.from_user.id
    TEMP.setdefault(uid, {})
    await message.answer(TEXT[get_lang(uid)]["choose_lang"], reply_markup=lang_kb())

# ================== ЯЗЫК ==================
@dp.callback_query(lambda c: c.data.startswith("lang:"))
async def set_lang(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = callback.data.split(":")[1]
    TEMP.setdefault(uid, {})["lang"] = lang
    
    await send_main_menu(callback, uid, lang)
    
    await callback.message.answer(
        "⬇️ Используйте кнопку ниже для возврата в главное меню"
        if lang == "ru" else
        "⬇️ Use the button below to return to the main menu",
        reply_markup=bottom_menu_kb(lang)
    )

# ================== НАЗАД В МЕНЮ ==================
@dp.message(lambda m: m.text in ("🔄 В главное меню", "🔄 Main menu"))
async def back_to_menu(message: types.Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    TEMP.setdefault(uid, {})
    TEMP[uid].pop("step", None)
    await send_main_menu(message, uid, lang)

# ================== КОНТАКТЫ ==================
@dp.callback_query(lambda c: c.data == "menu:contacts")
async def contacts(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    await callback.message.edit_text(TEXT[lang]["contacts"])

# ================== КОНСУЛЬТАЦИЯ ==================
@dp.callback_query(lambda c: c.data == "menu:consult")
async def consult_info(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✍️ Написать вопрос" if lang=="ru" else "✍️ Write question", callback_data="consult:start")
    ]])
    await callback.message.edit_text(TEXT[lang]["consult"], parse_mode="Markdown", reply_markup=kb)

@dp.callback_query(lambda c: c.data == "consult:start")
async def consult_start(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = get_lang(uid)
    TEMP[uid]["step"] = "consult"
    await callback.message.edit_text("✍️ Напишите ваш вопрос:" if lang=="ru" else "✍️ Write your question:")

# ================== АНКЕТА ==================
@dp.callback_query(lambda c: c.data == "menu:form")
async def form_start(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    await callback.message.edit_text("Есть ли у вас TLC-лицензия?" if lang=="ru" else "Do you have a TLC license?", reply_markup=yes_no_kb("tlc", lang))

@dp.callback_query(lambda c: c.data.startswith("tlc"))
async def q_tlc(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"): return await callback.message.edit_text(TEXT[lang]["fail"])
    await callback.message.edit_text("Стаж вождения в США 1+ год?" if lang=="ru" else "1+ year driving experience?", reply_markup=yes_no_kb("exp", lang))

@dp.callback_query(lambda c: c.data.startswith("exp"))
async def q_exp(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"): return await callback.message.edit_text(TEXT[lang]["fail"])
    await callback.message.edit_text("Вы ищете автомобиль в аренду?" if lang=="ru" else "Looking to rent a vehicle?", reply_markup=yes_no_kb("rent", lang))

@dp.callback_query(lambda c: c.data.startswith("rent"))
async def q_rent(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"): return await callback.message.edit_text(TEXT[lang]["fail"])
    await callback.message.edit_text("Подходит ли Toyota Sienna Hybrid (WAV)?" if lang=="ru" else "Is Toyota Sienna Hybrid (WAV) suitable?", reply_markup=yes_no_kb("car_final", lang))

@dp.callback_query(lambda c: c.data.startswith("car_final"))
async def q_car_final(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"): return await callback.message.edit_text(TEXT[lang]["fail"])
    await callback.message.edit_text(TEXT[lang]["success"], reply_markup=site_kb(lang))

# ================== РАБОЧЕЕ МЕНЮ (АВТОЗАПОЛНЕНИЕ НОМЕРА) ==================
@dp.callback_query(lambda c: c.data == "menu:work")
async def work_menu(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = get_lang(uid)
    if uid not in ALLOWED_DRIVERS: return await callback.message.edit_text(TEXT[lang]["no_access"])
    TEMP[uid].pop("step", None)
    await callback.message.edit_text(TEXT[lang]["work_intro"], reply_markup=work_menu_kb(lang))

@dp.callback_query(lambda c: c.data.startswith("work:"))
async def work_start(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = get_lang(uid)
    if uid not in ALLOWED_DRIVERS: return await callback.message.edit_text(TEXT[lang]["no_access"])
    
    action = callback.data.split(":")[1]
    if action == "info": return await callback.message.edit_text(TEXT[lang]["work_info"], parse_mode="Markdown")
    if action == "admin": return await callback.message.edit_text(TEXT[lang]["contacts"])

    # --- ЗДЕСЬ АВТОЗАПОЛНЕНИЕ ---
    TEMP[uid]["work_type"] = action
    TEMP[uid]["car"] = DRIVERS[uid]["car_number"]  # Номер берется из словаря DRIVERS автоматически
    TEMP[uid]["step"] = "work_photo"

    prompt = TEXT[lang]["ask_photo_dmv"] if action == "dmv" else TEXT[lang]["ask_photo_service"]
    await callback.message.edit_text(prompt)

# ================== ОБРАБОТЧИК СООБЩЕНИЙ ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id
    if uid not in TEMP: return
    lang = get_lang(uid)
    step = TEMP[uid].get("step")

    # Консультация
    if step == "consult":
        await bot.send_message(CHANNEL_ID, f"💼 Consultation\nID: {uid}\n@{message.from_user.username or 'no_user'}\n\n{message.text}")
        TEMP[uid]["step"] = None
        await message.answer(TEXT[lang]["consult_done"], reply_markup=bottom_menu_kb(lang))
        return

    # Рабочие процессы (только для разрешенных)
    if uid not in ALLOWED_DRIVERS: return

    # Шаг с фото
    if step == "work_photo":
        if not (message.photo or (message.document and (message.document.mime_type or "").startswith("image/"))):
            await message.answer("❗️ Фото обязательно. Пожалуйста, загрузите изображение.")
            return
        
        TEMP[uid]["photo"] = message.photo[-1].file_id if message.photo else message.document.file_id
        TEMP[uid]["step"] = "work_comment"
        await message.answer("✍️ Теперь введите комментарий или напишите '-':")
        return

    # Шаг с комментарием и отправка
    if step == "work_comment":
        if "work_type" not in TEMP[uid] or "car" not in TEMP[uid]:
            TEMP[uid].pop("step", None)
            return await message.answer("⚠️ Сессия устарела. Начните заново.")

        driver_info = DRIVERS[uid]
        caption = (
            f"🛠 {TEMP[uid]['work_type'].upper()}\n"
            f"👤 Имя: {driver_info['name']}\n"
            f"🚗 Авто: {driver_info['car_model']}\n"
            f"🔢 Номер: {TEMP[uid]['car']}\n"
            f"🆔 ID: {uid}\n"
            f"👤 User: @{message.from_user.username or 'none'}\n\n"
            f"💬 Коммент: {message.text}"
        )

        await bot.send_photo(CHANNEL_ID, TEMP[uid]["photo"], caption=caption)
        
        # Очистка
        TEMP[uid].pop("step", None)
        TEMP[uid].pop("work_type", None)
        TEMP[uid].pop("photo", None)
        TEMP[uid].pop("car", None)

        await message.answer(TEXT[lang]["sent"], reply_markup=bottom_menu_kb(lang))

# ================== ЗАПУСК ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

