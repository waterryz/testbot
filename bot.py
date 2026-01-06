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
# user_id: {"lang": "ru/en", "step": "...", "car": str}

# ================== ТЕКСТЫ ==================
TEXT = {
    "ru": {
        "welcome_new": (
            "👋 Добро пожаловать в Prime Fusion!\n\n"
            "• Если вы *новый клиент* — пройдите анкету\n"
            "• Если хотите *разместить свои автомобили на сайте* — "
            "свяжитесь с нами через контакты"
        ),
        "welcome_allowed": (
            "👋 Добро пожаловать в Prime Fusion!\n\n"
            "Вы находитесь в рабочем пространстве арендодатора.\n"
            "Используйте рабочее меню для связи с администрацией."
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
        "site": "🚗 Перейти на сайт"
    },
    "en": {
        "welcome_new": (
            "👋 Welcome to Prime Fusion!\n\n"
            "• If you are a *new client* — please fill out the form\n"
            "• If you want to *list your vehicles on our website* — "
            "contact us via Contacts"
        ),
        "welcome_allowed": (
            "👋 Welcome to Prime Fusion!\n\n"
            "You are in the landlord workspace.\n"
            "Use the work menu to contact administration."
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
        "site": "🚗 Go to website"
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
        [InlineKeyboardButton(text="📝 Анкета" if lang == "ru" else "📝 Form", callback_data="menu:form")],
        [InlineKeyboardButton(text="📞 Контакты" if lang == "ru" else "📞 Contacts", callback_data="menu:contacts")]
    ])

def menu_allowed_user_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧰 Рабочее меню" if lang == "ru" else "🧰 Work menu", callback_data="menu:work")]
    ])

def yes_no_kb(step, lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да" if lang == "ru" else "✅ Yes", callback_data=f"{step}:yes"),
            InlineKeyboardButton(text="❌ Нет" if lang == "ru" else "❌ No", callback_data=f"{step}:no")
        ]
    ])

def site_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=TEXT[lang]["site"],
            web_app=WebAppInfo(url=SITE_URL)
        )]
    ])

def bottom_menu_kb(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 В главное меню" if lang == "ru" else "🔄 Main menu")]],
        resize_keyboard=True
    )

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    TEMP[message.from_user.id] = {}
    await message.answer(
        "🌐 Выберите язык / Choose language",
        reply_markup=lang_kb()
    )

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

# ================== КОНТАКТЫ ==================
@dp.callback_query(lambda c: c.data == "menu:contacts")
async def contacts(callback: types.CallbackQuery):
    lang = TEMP[callback.from_user.id]["lang"]
    await callback.message.edit_text(TEXT[lang]["contacts"])

# ================== АНКЕТА ==================
@dp.callback_query(lambda c: c.data == "menu:form")
async def form_start(callback: types.CallbackQuery):
    lang = TEMP[callback.from_user.id]["lang"]
    await callback.message.edit_text(
        "Есть ли у вас TLC-лицензия?" if lang == "ru" else "Do you have a TLC license?",
        reply_markup=yes_no_kb("tlc", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("tlc"))
async def q_tlc(callback: types.CallbackQuery):
    lang = TEMP[callback.from_user.id]["lang"]
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        "Стаж вождения в США 1+ год?" if lang == "ru" else "Driving experience in the US 1+ year?",
        reply_markup=yes_no_kb("exp", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("exp"))
async def q_exp(callback: types.CallbackQuery):
    lang = TEMP[callback.from_user.id]["lang"]
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        "Вы ищете автомобиль в аренду?" if lang == "ru" else "Are you looking to rent a vehicle?",
        reply_markup=yes_no_kb("rent", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("rent"))
async def q_rent(callback: types.CallbackQuery):
    lang = TEMP[callback.from_user.id]["lang"]
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        "Подходит ли Toyota Sienna Hybrid (VAN)?" if lang == "ru" else "Is Toyota Sienna Hybrid (VAN) suitable?",
        reply_markup=yes_no_kb("car", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("car"))
async def q_car(callback: types.CallbackQuery):
    lang = TEMP[callback.from_user.id]["lang"]
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        TEXT[lang]["success"],
        reply_markup=site_kb(lang)
    )

# ================== РАБОЧЕЕ МЕНЮ ==================
@dp.callback_query(lambda c: c.data == "menu:work")
async def work_menu(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = TEMP[uid]["lang"]

    TEMP[uid]["step"] = "car"

    await callback.message.edit_text(
        "Введите номер автомобиля:" if lang == "ru" else "Enter vehicle number:"
    )
    await callback.message.answer(
        "Вы можете вернуться в меню 👇" if lang == "ru" else "You can return to menu 👇",
        reply_markup=bottom_menu_kb(lang)
    )

# ================== СООБЩЕНИЯ ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id
    if uid not in TEMP or "step" not in TEMP[uid]:
        return

    lang = TEMP[uid]["lang"]

    if TEMP[uid]["step"] == "car":
        TEMP[uid]["car"] = message.text.strip()
        TEMP[uid]["step"] = "msg"
        await message.answer(
            "✍️ Напишите сообщение администрации:" if lang == "ru"
            else "✍️ Write a message to administration:"
        )
        return

    if TEMP[uid]["step"] == "msg":
        text = (
            "🚗 Сообщение от арендодатора\n\n"
            f"Авто: {TEMP[uid]['car']}\n"
            f"ID: {uid}\n"
            f"Username: @{message.from_user.username or 'none'}\n\n"
            f"Сообщение:\n{message.text}"
        )

        await bot.send_message(CHANNEL_ID, text)

        await message.answer(
            "✅ Сообщение отправлено." if lang == "ru"
            else "✅ Message sent.",
            reply_markup=bottom_menu_kb(lang)
        )

# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
