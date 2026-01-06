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
# user_id: {"lang":"ru/en", "step":"work_car|work_text|work_photo", "car":str, "text":str}

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
            "Вы в рабочем пространстве арендодатора."
        ),
        "contacts": (
            "📞 Контакты для сотрудничества:\n\n"
            "Telegram: @primefusion_admin\n"
            "Email: info@primefusioncars.com"
        ),
        "fail": "❌ К сожалению, на данный момент сервис вам не подходит.",
        "success": "✅ Вы подходите под условия.\n\nПерейдите на сайт.",
        "site": "🚗 Перейти на сайт",

        "work_intro": (
            "🧰 Рабочее меню\n\n"
            "🛠 *Напоминание:* сервис нужно делать *раз в 2 месяца*.\n"
            "После сервиса *обязательно загрузите фото* "
            "(чек / одометр / выполненные работы)."
        ),
        "ask_car": "🚗 Введите номер автомобиля:",
        "ask_text": "✍️ Введите сообщение (описание сервиса / комментарий):",
        "ask_photo": (
            "📸 Загрузите *фото сервиса*.\n"
            "Фото обязательно. Можно отправить несколько."
        ),
        "sent": "✅ Сообщение и фото отправлены администрации.",
        "no_access": "⛔️ У вас нет доступа."
    },
    "en": {
        "choose_lang": "🌐 Choose language / Выберите язык",
        "welcome_new": (
            "👋 Welcome to Prime Fusion!\n\n"
            "• If you are a *new client* — fill out the form\n"
            "• If you want to *list vehicles* — contact us"
        ),
        "welcome_allowed": (
            "👋 Welcome to Prime Fusion!\n\n"
            "You are in the landlord workspace."
        ),
        "contacts": (
            "📞 Contacts:\n\n"
            "Telegram: @primefusion_admin\n"
            "Email: info@primefusioncars.com"
        ),
        "fail": "❌ Unfortunately, the service is not available.",
        "success": "✅ You meet the requirements.\n\nVisit the website.",
        "site": "🚗 Go to website",

        "work_intro": (
            "🧰 Work menu\n\n"
            "🛠 *Reminder:* service every *2 months*.\n"
            "After service you must *upload photos*."
        ),
        "ask_car": "🚗 Enter vehicle number:",
        "ask_text": "✍️ Enter message (service description):",
        "ask_photo": (
            "📸 Upload *service photos*.\n"
            "Photos are mandatory. You can send multiple."
        ),
        "sent": "✅ Message and photos sent to administration.",
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

def menu_new_user_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Анкета" if lang=="ru" else "📝 Form", callback_data="menu:form")],
        [InlineKeyboardButton(text="📞 Контакты" if lang=="ru" else "📞 Contacts", callback_data="menu:contacts")]
    ])

def menu_allowed_user_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧰 Рабочее меню" if lang=="ru" else "🧰 Work menu", callback_data="menu:work")]
    ])

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

def bottom_menu_kb(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 В главное меню" if lang=="ru" else "🔄 Main menu")]],
        resize_keyboard=True
    )

def get_lang(uid):
    return TEMP.get(uid, {}).get("lang", "ru")

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    TEMP[message.from_user.id] = {}
    await message.answer(TEXT["ru"]["choose_lang"], reply_markup=lang_kb())

# ================== LANGUAGE ==================
@dp.callback_query(lambda c: c.data.startswith("lang:"))
async def set_lang(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = callback.data.split(":")[1]
    TEMP.setdefault(uid, {})["lang"] = lang

    if uid in ALLOWED_DRIVERS:
        await callback.message.edit_text(
            TEXT[lang]["welcome_allowed"],
            reply_markup=menu_allowed_user_kb(lang)
        )
    else:
        await callback.message.edit_text(
            TEXT[lang]["welcome_new"],
            parse_mode="Markdown",
            reply_markup=menu_new_user_kb(lang)
        )

# ================== ВОЗВРАТ В МЕНЮ ==================
@dp.message(lambda m: m.text in ("🔄 В главное меню", "🔄 Main menu"))
async def back_to_menu(message: types.Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    TEMP[uid] = {"lang": lang}
    if uid in ALLOWED_DRIVERS:
        await message.answer(TEXT[lang]["welcome_allowed"], reply_markup=menu_allowed_user_kb(lang))
    else:
        await message.answer(TEXT[lang]["welcome_new"], parse_mode="Markdown", reply_markup=menu_new_user_kb(lang))

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
        "Есть ли у вас TLC-лицензия?" if lang=="ru" else "Do you have a TLC license?",
        reply_markup=yes_no_kb("tlc", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("tlc"))
async def q_tlc(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        "Стаж вождения в США 1+ год?" if lang=="ru" else "1+ year driving experience?",
        reply_markup=yes_no_kb("exp", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("exp"))
async def q_exp(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        "Вы ищете автомобиль в аренду?" if lang=="ru" else "Looking to rent a vehicle?",
        reply_markup=yes_no_kb("rent", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("rent"))
async def q_rent(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        "Подходит ли Toyota Sienna Hybrid?" if lang=="ru" else "Is Toyota Sienna Hybrid suitable?",
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

    TEMP[uid]["step"] = "work_car"
    await callback.message.edit_text(TEXT[lang]["work_intro"], parse_mode="Markdown")
    await callback.message.answer(TEXT[lang]["ask_car"], reply_markup=bottom_menu_kb(lang))

# ================== ОСНОВНАЯ ЦЕПОЧКА ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id
    if uid not in TEMP or uid not in ALLOWED_DRIVERS:
        return

    lang = get_lang(uid)
    step = TEMP[uid].get("step")

    if step == "work_car":
        TEMP[uid]["car"] = message.text.strip()
        TEMP[uid]["step"] = "work_text"
        await message.answer(TEXT[lang]["ask_text"])
        return

    if step == "work_text":
        TEMP[uid]["text"] = message.text.strip()
        TEMP[uid]["step"] = "work_photo"
        await message.answer(TEXT[lang]["ask_photo"], parse_mode="Markdown")
        return

    if step == "work_photo":
        car = TEMP[uid]["car"]
        text_msg = TEMP[uid]["text"]

        caption = (
            "🛠 Сообщение / Сервис\n\n"
            f"Авто: {car}\n"
            f"ID: {uid}\n"
            f"Username: @{message.from_user.username or 'нет'}\n\n"
            f"Комментарий:\n{text_msg}"
        )

    # ✅ ЕСЛИ ПРИСЛАЛИ ФОТО — ОТПРАВЛЯЕМ ФОТО
    if message.photo:
        await bot.send_photo(
            CHANNEL_ID,
            message.photo[-1].file_id,
            caption=caption
        )
        TEMP[uid]["step"] = None
        await message.answer(TEXT[lang]["sent"], reply_markup=ReplyKeyboardRemove())
        return

    if message.document and (message.document.mime_type or "").startswith("image/"):
        await bot.send_document(
            CHANNEL_ID,
            message.document.file_id,
            caption=caption
        )
        TEMP[uid]["step"] = None
        await message.answer(TEXT[lang]["sent"], reply_markup=ReplyKeyboardRemove())
        return

    # ✅ ЕСЛИ ВВЕЛИ "-" ИЛИ ЛЮБОЙ ТЕКСТ — ФОТО НЕТ, ПРОСТО ОТПРАВЛЯЕМ ТЕКСТ
    if message.text:
        await bot.send_message(CHANNEL_ID, caption)
        TEMP[uid]["step"] = None
        await message.answer(TEXT[lang]["sent"], reply_markup=ReplyKeyboardRemove())
        return
# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


