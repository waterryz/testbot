import asyncio
from aiogram import Bot, Dispatcher, types
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

ALLOWED_DRIVERS = {5348697217, 547004364}

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== TEMP ==================
TEMP = {}
# user_id: {"lang":"ru/en", "step":"...", "car":str, "text":str}

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
            "🛠 Сервис нужно делать раз в 7000 миль.\n"
            "Фото можно прикрепить при наличии."
        ),

        "ask_car": "🚗 Введите номер автомобиля:",
        "ask_text": "✍️ Введите сообщение:",
        "ask_photo": "📸 Загрузите фото.",
        "sent": "✅ Сообщение отправлено администрации.",
        "no_access": "⛔️ У вас нет доступа."
    },

    "en": {
        "choose_lang": "🌐 Choose language",

        "welcome_new": (
            "👋 Welcome to Prime Fusion!\n\n"
            "• New client — fill out the form\n"
            "• Want to list vehicles — contact us"
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
            "🛠 Service every 7000 miles.\n"
            "Photos optional."
        ),

        "ask_car": "🚗 Enter vehicle number:",
        "ask_text": "✍️ Enter message:",
        "ask_photo": "📸 Upload photo.",
        "sent": "✅ Message sent.",
        "no_access": "⛔️ No access."
    }
}

# ================== КЛАВИАТУРЫ ==================
def bottom_menu_kb(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 В главное меню" if lang == "ru" else "🔄 Main menu")]],
        resize_keyboard=True
    )

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
        [InlineKeyboardButton(text="💼 Консультация" if lang=="ru" else "💼 Consultation", callback_data="menu:consult")]
    ])

def consult_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✍️ Написать вопрос" if lang=="ru" else "✍️ Write question",
            callback_data="consult:start"
        )]
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

def get_lang(uid):
    return TEMP.get(uid, {}).get("lang", "ru")

# ================== START (FIXED) ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    uid = message.from_user.id
    TEMP.setdefault(uid, {})   # ❗️НЕ стираем lang
    await message.answer(
        TEXT[get_lang(uid)]["choose_lang"],
        reply_markup=lang_kb()
    )

# ================== LANGUAGE ==================
@dp.callback_query(lambda c: c.data.startswith("lang:"))
async def set_lang(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = callback.data.split(":")[1]
    TEMP.setdefault(uid, {})["lang"] = lang

    if uid in ALLOWED_DRIVERS:
        await callback.message.edit_text(TEXT[lang]["welcome_allowed"],
                                         reply_markup=menu_allowed_user_kb(lang))
    else:
        await callback.message.edit_text(TEXT[lang]["welcome_new"],
                                         parse_mode="Markdown",
                                         reply_markup=menu_new_user_kb(lang))

# ================== BACK TO MENU ==================
@dp.message(lambda m: m.text in ("🔄 В главное меню", "🔄 Main menu"))
async def back_to_menu(message: types.Message):
    uid = message.from_user.id
    lang = get_lang(uid)
    TEMP.setdefault(uid, {})
    TEMP[uid]["lang"] = lang
    TEMP[uid].pop("step", None)


    if uid in ALLOWED_DRIVERS:
        await message.answer(TEXT[lang]["welcome_allowed"],
                             reply_markup=menu_allowed_user_kb(lang))
    else:
        await message.answer(TEXT[lang]["welcome_new"],
                             parse_mode="Markdown",
                             reply_markup=menu_new_user_kb(lang))

# ================== CONTACTS ==================
@dp.callback_query(lambda c: c.data == "menu:contacts")
async def contacts(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    await callback.message.edit_text(TEXT[lang]["contacts"])

# ================== CONSULT ==================
@dp.callback_query(lambda c: c.data == "menu:consult")
async def consult_info(callback: types.CallbackQuery):
    lang = get_lang(callback.from_user.id)
    await callback.message.edit_text(TEXT[lang]["consult"],
                                     parse_mode="Markdown",
                                     reply_markup=consult_kb(lang))

@dp.callback_query(lambda c: c.data == "consult:start")
async def consult_start(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = get_lang(uid)
    TEMP.setdefault(uid, {})["step"] = "consult"
    await callback.message.edit_text(
        "✍️ Напишите ваш вопрос:" if lang=="ru"
        else "✍️ Write your question:"
    )

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

# ================== WORK MENU ==================
@dp.callback_query(lambda c: c.data == "menu:work")
async def work_menu(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = get_lang(uid)

    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text(TEXT[lang]["no_access"])
        return

    TEMP[uid]["step"] = "work_car"
    await callback.message.edit_text(TEXT[lang]["work_intro"])
    await callback.message.answer(TEXT[lang]["ask_car"], reply_markup=bottom_menu_kb(lang))

# ================== HANDLE MESSAGES ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id
    if uid not in TEMP:
        return

    lang = get_lang(uid)
    step = TEMP[uid].get("step")

    if step == "consult":
        await bot.send_message(
            CHANNEL_ID,
            f"💼 Consultation\nID: {uid}\n@{message.from_user.username}\n\n{message.text}"
        )
        TEMP[uid]["step"] = None
        await message.answer(TEXT[lang]["consult_done"], reply_markup=bottom_menu_kb(lang))
        return

    if uid not in ALLOWED_DRIVERS:
        return

    if step == "work_car":
        TEMP[uid]["car"] = message.text
        TEMP[uid]["step"] = "work_text"
        await message.answer(TEXT[lang]["ask_text"], reply_markup=bottom_menu_kb(lang))
        return

    if step == "work_text":
        TEMP[uid]["text"] = message.text
        TEMP[uid]["step"] = "work_photo"
        await message.answer(TEXT[lang]["ask_photo"], reply_markup=bottom_menu_kb(lang))
        return

    if step == "work_photo":
        caption = (
            "🛠 Service report\n\n"
            f"Car: {TEMP[uid]['car']}\n"
            f"ID: {uid}\n"
            f"@{message.from_user.username or 'no_username'}\n\n"
            f"{TEMP[uid]['text']}"
        )

    # ✅ Фото
        if message.photo:
            await bot.send_photo(
                CHANNEL_ID,
                message.photo[-1].file_id,
                caption=caption
            )

    # ✅ Фото как файл
        elif message.document and (message.document.mime_type or "").startswith("image/"):
            await bot.send_document(
                CHANNEL_ID,
                message.document.file_id,
                caption=caption
            )

    # ❌ ВСЁ ОСТАЛЬНОЕ — ЗАПРЕЩЕНО
        else:
            await message.answer(
                "❗️Фото обязательно. Без фото отправка невозможна.\n"
                if lang == "ru" else
                    "❗️Photo is required. Submission without photo is not allowed.",
                reply_markup=bottom_menu_kb(lang)
            )
            return  # ⛔️ НЕ ВЫХОДИМ ИЗ ШАГА

    # ✅ Фото получено — завершаем
        TEMP[uid]["step"] = None
        await message.answer(
            TEXT[lang]["sent"],
            reply_markup=bottom_menu_kb(lang)
        )


# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




