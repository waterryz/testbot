import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    WebAppInfo
)

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8550400671:AAHZdPJcWi_NtkurCHGxUgmRsQKMTu3826g"
CHANNEL_ID = -1003580316890
SITE_URL = "https://www.primefusioncars.com/"

ALLOWED_DRIVERS = {5348697217, 547004364}

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== TEMP ==================
TEMP = {}
# user_id: {"lang":"ru/en", "step":"...", "car":"..."}

# ================== ТЕКСТЫ ==================
TEXT = {
    "ru": {
        "choose_lang": "🌐 Выберите язык / Choose language",
        "welcome_new": (
            "👋 Добро пожаловать в Prime Fusion!\n\n"
            "• Если вы *новый клиент* — пройдите анкету\n"
            "• Если хотите *разместить свои автомобили на сайте* — свяжитесь с нами через контакты"
        ),
        "welcome_allowed": (
            "👋 Добро пожаловать в Prime Fusion!\n\n"
            "Вы в рабочем пространстве арендодатора.\n"
            "Откройте рабочее меню для задач и связи с администрацией."
        ),
        "contacts": (
            "📞 Контакты для сотрудничества:\n\n"
            "Telegram: @primefusion_admin\n"
            "Email: info@primefusioncars.com"
        ),
        "fail": "❌ К сожалению, на данный момент сервис вам не подходит.",
        "success": (
            "✅ Вы подходите под условия.\n\n"
            "Перейдите на сайт для получения полной информации."
        ),
        "site": "🚗 Перейти на сайт",

        "work_intro": (
            "🧰 Рабочее меню\n\n"
            "🛠 *Напоминание:* сервис нужно делать *раз в 2 месяца*.\n"
            "После сервиса обязательно *загрузите фото* (чек/одометр/работы) — они уйдут администрации."
        ),
        "ask_car": "🚗 Введите номер автомобиля:",
        "saved_car": "✅ Авто сохранено: ",
        "work_choose": "Выберите действие 👇",
        "write_admin": "✍️ Напишите сообщение администрации:",
        "sent_admin": "✅ Сообщение отправлено администрации.",
        "upload_hint": (
            "📸 Отправьте *фото сервиса* сюда (можно несколько).\n"
            "Когда закончите — нажмите *Готово*."
        ),
        "photo_sent": "✅ Фото отправлено администрации. Можете отправить ещё или нажать *Готово*.",
        "done_upload": "✅ Загрузка завершена. Выберите действие 👇",
        "no_access": "⛔️ У вас нет доступа."
    },
    "en": {
        "choose_lang": "🌐 Choose language / Выберите язык",
        "welcome_new": (
            "👋 Welcome to Prime Fusion!\n\n"
            "• If you are a *new client* — please fill out the form\n"
            "• If you want to *list your vehicles on our website* — contact us via Contacts"
        ),
        "welcome_allowed": (
            "👋 Welcome to Prime Fusion!\n\n"
            "You are in the landlord workspace.\n"
            "Open the work menu for tasks and to contact administration."
        ),
        "contacts": (
            "📞 Contacts for partnership:\n\n"
            "Telegram: @primefusion_admin\n"
            "Email: info@primefusioncars.com"
        ),
        "fail": "❌ Unfortunately, the service is not available for you.",
        "success": (
            "✅ You meet the requirements.\n\n"
            "Visit the website for full details."
        ),
        "site": "🚗 Go to website",

        "work_intro": (
            "🧰 Work menu\n\n"
            "🛠 *Reminder:* service must be done *every 2 months*.\n"
            "After service please *upload photos* (receipt/odometer/work done) — they will be sent to admin."
        ),
        "ask_car": "🚗 Enter vehicle number:",
        "saved_car": "✅ Vehicle saved: ",
        "work_choose": "Choose an action 👇",
        "write_admin": "✍️ Write a message to administration:",
        "sent_admin": "✅ Message sent to administration.",
        "upload_hint": (
            "📸 Send *service photos* here (you can send multiple).\n"
            "When finished — press *Done*."
        ),
        "photo_sent": "✅ Photo sent to admin. Send more or press *Done*.",
        "done_upload": "✅ Upload finished. Choose an action 👇",
        "no_access": "⛔️ You have no access."
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

def menu_new_user_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Анкета" if lang == "ru" else "📝 Form", callback_data="menu:form")],
        [InlineKeyboardButton(text="📞 Контакты" if lang == "ru" else "📞 Contacts", callback_data="menu:contacts")]
    ])

def menu_allowed_user_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧰 Рабочее меню" if lang == "ru" else "🧰 Work menu", callback_data="menu:work")]
    ])

def yes_no_kb(step: str, lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да" if lang == "ru" else "✅ Yes", callback_data=f"{step}:yes"),
            InlineKeyboardButton(text="❌ Нет" if lang == "ru" else "❌ No", callback_data=f"{step}:no")
        ]
    ])

def site_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=TEXT[lang]["site"], web_app=WebAppInfo(url=SITE_URL))]
    ])

def work_actions_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✉️ Сообщение администрации" if lang == "ru" else "✉️ Message to admin",
                              callback_data="work:msg")],
        [InlineKeyboardButton(text="📸 Загрузить фото сервиса" if lang == "ru" else "📸 Upload service photos",
                              callback_data="work:photos")],
    ])

def bottom_menu_kb(lang: str, uploading: bool = False):
    row = []
    row.append(KeyboardButton(text="🔄 В главное меню" if lang == "ru" else "🔄 Main menu"))
    if uploading:
        row.append(KeyboardButton(text="✅ Готово" if lang == "ru" else "✅ Done"))
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

# ================== UTILS ==================
def get_lang(uid: int) -> str:
    return TEMP.get(uid, {}).get("lang", "ru")

async def show_main_menu(message_or_callback: types.Message | types.CallbackQuery):
    uid = message_or_callback.from_user.id
    lang = get_lang(uid)

    if uid in ALLOWED_DRIVERS:
        text = TEXT[lang]["welcome_allowed"]
        kb = menu_allowed_user_kb(lang)
        if isinstance(message_or_callback, types.CallbackQuery):
            await message_or_callback.message.edit_text(text, reply_markup=kb)
        else:
            await message_or_callback.answer(text, reply_markup=kb)
    else:
        text = TEXT[lang]["welcome_new"]
        kb = menu_new_user_kb(lang)
        if isinstance(message_or_callback, types.CallbackQuery):
            await message_or_callback.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await message_or_callback.answer(text, parse_mode="Markdown", reply_markup=kb)

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    uid = message.from_user.id
    TEMP[uid] = {}  # сбрасываем состояние
    await message.answer(TEXT["ru"]["choose_lang"], reply_markup=lang_kb())

# ================== LANGUAGE ==================
@dp.callback_query(lambda c: c.data.startswith("lang:"))
async def set_lang(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = callback.data.split(":")[1]
    TEMP.setdefault(uid, {})["lang"] = lang
    TEMP[uid].pop("step", None)
    # показываем меню по роли
    await show_main_menu(callback)

# ================== ВОЗВРАТ В ГЛАВНОЕ МЕНЮ ==================
@dp.message(lambda m: m.text in ("🔄 В главное меню", "🔄 Main menu"))
async def back_to_menu(message: types.Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    TEMP.setdefault(uid, {})  # не убиваем язык
    TEMP[uid].pop("step", None)
    await message.answer("✅" if lang == "ru" else "✅", reply_markup=ReplyKeyboardRemove())
    await show_main_menu(message)

# ================== КОНТАКТЫ ==================
@dp.callback_query(lambda c: c.data == "menu:contacts")
async def contacts(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    await callback.message.edit_text(TEXT[lang]["contacts"])

# ================== АНКЕТА ==================
@dp.callback_query(lambda c: c.data == "menu:form")
async def form_start(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    await callback.message.edit_text(
        "Есть ли у вас TLC-лицензия?" if lang == "ru" else "Do you have a TLC license?",
        reply_markup=yes_no_kb("tlc", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("tlc"))
async def q_tlc(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        "Стаж вождения в США 1+ год?" if lang == "ru" else "Driving experience in the US 1+ year?",
        reply_markup=yes_no_kb("exp", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("exp"))
async def q_exp(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        "Вы ищете автомобиль в аренду?" if lang == "ru" else "Are you looking to rent a vehicle?",
        reply_markup=yes_no_kb("rent", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("rent"))
async def q_rent(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        "Подходит ли Toyota Sienna Hybrid (VAN)?" if lang == "ru" else "Is Toyota Sienna Hybrid (VAN) suitable?",
        reply_markup=yes_no_kb("car", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("car"))
async def q_car(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(TEXT[lang]["success"], reply_markup=site_kb(lang))

# ================== РАБОЧЕЕ МЕНЮ ==================
@dp.callback_query(lambda c: c.data == "menu:work")
async def work_menu(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = get_lang(uid)

    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text(TEXT[lang]["no_access"])
        return

    TEMP.setdefault(uid, {})["step"] = "work_car"

    await callback.message.edit_text(TEXT[lang]["work_intro"], parse_mode="Markdown")
    await callback.message.answer(TEXT[lang]["ask_car"], reply_markup=bottom_menu_kb(lang))

# ================== WORK ACTIONS ==================
@dp.callback_query(lambda c: c.data == "work:msg")
async def work_message_start(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = get_lang(uid)

    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text(TEXT[lang]["no_access"])
        return

    if not TEMP.get(uid, {}).get("car"):
        TEMP.setdefault(uid, {})["step"] = "work_car"
        await callback.message.edit_text(TEXT[lang]["ask_car"])
        return

    TEMP[uid]["step"] = "work_msg"
    await callback.message.edit_text(TEXT[lang]["write_admin"])

@dp.callback_query(lambda c: c.data == "work:photos")
async def work_photos_start(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = get_lang(uid)

    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text(TEXT[lang]["no_access"])
        return

    if not TEMP.get(uid, {}).get("car"):
        TEMP.setdefault(uid, {})["step"] = "work_car"
        await callback.message.edit_text(TEXT[lang]["ask_car"])
        return

    TEMP[uid]["step"] = "work_photos"
    await callback.message.edit_text(TEXT[lang]["upload_hint"], parse_mode="Markdown")
    await callback.message.answer(
        "👇" if lang == "ru" else "👇",
        reply_markup=bottom_menu_kb(lang, uploading=True)
    )

# ================== DONE UPLOAD ==================
@dp.message(lambda m: m.text in ("✅ Готово", "✅ Done"))
async def done_upload(message: types.Message):
    uid = message.from_user.id
    lang = get_lang(uid)

    if uid not in ALLOWED_DRIVERS:
        return

    if TEMP.get(uid, {}).get("step") != "work_photos":
        return

    TEMP[uid]["step"] = "work_idle"
    await message.answer(
        TEXT[lang]["done_upload"],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        TEXT[lang]["work_choose"],
        reply_markup=work_actions_kb(lang)
    )

# ================== ОБРАБОТКА СООБЩЕНИЙ/ФОТО ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id
    if uid not in TEMP:
        return

    lang = get_lang(uid)
    step = TEMP[uid].get("step")

    # --- ввод номера авто ---
    if step == "work_car":
        car = message.text.strip()
        TEMP[uid]["car"] = car
        TEMP[uid]["step"] = "work_idle"

        await message.answer(
            TEXT[lang]["saved_car"] + car,
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            TEXT[lang]["work_choose"],
            reply_markup=work_actions_kb(lang)
        )
        return

    # --- сообщение администрации ---
    if step == "work_msg":
        car = TEMP[uid].get("car", "—")
        text = (
            "✉️ Сообщение от арендодатора\n\n"
            f"Авто: {car}\n"
            f"ID: {uid}\n"
            f"Username: @{message.from_user.username or 'нет'}\n\n"
            f"Сообщение:\n{message.text}"
        )
        await bot.send_message(CHANNEL_ID, text)

        TEMP[uid]["step"] = "work_idle"
        await message.answer(TEXT[lang]["sent_admin"], reply_markup=ReplyKeyboardRemove())
        await message.answer(TEXT[lang]["work_choose"], reply_markup=work_actions_kb(lang))
        return

    # --- фото сервиса ---
    if step == "work_photos":
        car = TEMP[uid].get("car", "—")

        caption_ru = (
            "📸 Фото сервиса\n\n"
            f"Авто: {car}\n"
            f"ID: {uid}\n"
            f"Username: @{message.from_user.username or 'нет'}"
        )
        caption_en = (
            "📸 Service photo\n\n"
            f"Vehicle: {car}\n"
            f"ID: {uid}\n"
            f"Username: @{message.from_user.username or 'none'}"
        )
        caption = caption_ru if lang == "ru" else caption_en

        # Фото
        if message.photo:
            file_id = message.photo[-1].file_id
            await bot.send_photo(CHANNEL_ID, file_id, caption=caption)
            await message.answer(TEXT[lang]["photo_sent"], parse_mode="Markdown",
                                 reply_markup=bottom_menu_kb(lang, uploading=True))
            return

        # Документ (например фото как файл)
        if message.document and (message.document.mime_type or "").startswith("image/"):
            await bot.send_document(CHANNEL_ID, message.document.file_id, caption=caption)
            await message.answer(TEXT[lang]["photo_sent"], parse_mode="Markdown",
                                 reply_markup=bottom_menu_kb(lang, uploading=True))
            return

        # Если прислали не фото
        await message.answer(
            "❗️Пришлите фото (или файл-картинку) либо нажмите «Готово»."
            if lang == "ru" else
            "❗️Send a photo (or image file) or press “Done”.",
            reply_markup=bottom_menu_kb(lang, uploading=True)
        )
        return

# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
