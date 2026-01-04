import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8550400671:AAHZdPJcWi_NtkurCHGxUgmRsQKMTu3826g"
CHANNEL_ID = -1001234567890  # канал администраторов
SITE_URL = "https://www.primefusioncars.com/"

# Telegram ID действующих водителей
ALLOWED_DRIVERS = {
    5348697217,
    222222222,
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ================== ТЕКСТЫ ==================
TEXT = {
    "ru": {
        "welcome": "Проверим, подходите ли вы для аренды авто.",
        "tlc": "У вас есть TLC-лицензия?",
        "exp": "Стаж вождения в США 1+ год?",
        "rent": "Вы ищете автомобиль в аренду?",
        "car": "Вам подходит Toyota Sienna Hybrid (VAW)?",
        "fail": "❌ К сожалению, вы не подходите под условия.",
        "success": "✅ Вы подходите!\n\nПерейдите на сайт для бронирования.",
        "site": "🚗 Перейти на сайт"
    },
    "en": {
        "welcome": "Let’s check if you qualify for renting a vehicle.",
        "tlc": "Do you have a TLC license?",
        "exp": "Do you have 1+ year driving experience in the USA?",
        "rent": "Are you looking for a rental car?",
        "car": "Is Toyota Sienna Hybrid (VAW) suitable for you?",
        "fail": "❌ Sorry, you do not meet the requirements.",
        "success": "✅ You qualify!\n\nGo to the website for booking.",
        "site": "🚗 Go to website"
    }
}

# ================== КНОПКИ ==================
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆕 Новый арендатор", callback_data="role:new")],
        [InlineKeyboardButton(text="🚗 Действующий водитель", callback_data="role:active")]
    ])

def lang_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang:en"),
        ]
    ])

def yes_no_kb(step: str, lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yes", callback_data=f"{step}:yes:{lang}"),
            InlineKeyboardButton(text="❌ No", callback_data=f"{step}:no:{lang}"),
        ]
    ])

def site_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=TEXT[lang]["site"], web_app=WebAppInfo(url=SITE_URL))]
    ])

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Выберите, кто вы:",
        reply_markup=main_menu_kb()
    )

# ================== РОЛИ ==================
@dp.callback_query(lambda c: c.data == "role:new")
async def role_new(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Choose language / Выберите язык:",
        reply_markup=lang_kb()
    )

@dp.callback_query(lambda c: c.data == "role:active")
async def role_active(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in ALLOWED_DRIVERS:
        await callback.message.edit_text(
            "⛔️ Доступ запрещён.\n\n"
            "Отправьте ваш Telegram ID администрации."
        )
        return

    await callback.message.edit_text(
        "✅ Доступ подтверждён.\n\n"
        "Отправьте сообщение по работе:\n"
        "• ремонт\n• авария\n• вопрос\n• запрос"
    )

# ================== АНКЕТА ==================
@dp.callback_query(lambda c: c.data.startswith("lang"))
async def choose_lang(callback: types.CallbackQuery):
    lang = callback.data.split(":")[1]
    await callback.message.edit_text(
        TEXT[lang]["welcome"],
        reply_markup=yes_no_kb("tlc", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("tlc"))
async def q_tlc(callback: types.CallbackQuery):
    _, answer, lang = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(TEXT[lang]["exp"], reply_markup=yes_no_kb("exp", lang))

@dp.callback_query(lambda c: c.data.startswith("exp"))
async def q_exp(callback: types.CallbackQuery):
    _, answer, lang = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(TEXT[lang]["rent"], reply_markup=yes_no_kb("rent", lang))

@dp.callback_query(lambda c: c.data.startswith("rent"))
async def q_rent(callback: types.CallbackQuery):
    _, answer, lang = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(TEXT[lang]["car"], reply_markup=yes_no_kb("car", lang))

@dp.callback_query(lambda c: c.data.startswith("car"))
async def q_car(callback: types.CallbackQuery):
    _, answer, lang = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT[lang]["fail"])
        return

    await callback.message.edit_text(
        TEXT[lang]["success"],
        reply_markup=site_kb(lang)
    )

# ================== СООБЩЕНИЯ ОТ ВОДИТЕЛЕЙ ==================
@dp.message()
async def handle_driver_messages(message: types.Message):
    if message.from_user.id not in ALLOWED_DRIVERS:
        return

    text = (
        "🚗 Сообщение от водителя\n\n"
        f"👤 @{message.from_user.username or 'без username'}\n"
        f"🆔 {message.from_user.id}\n\n"
        f"💬 {message.text}"
    )

    await bot.send_message(CHANNEL_ID, text)
    await message.answer("✅ Принято. Информация передана администрации.")

# ================== RUN ==================
@dp.message()
async def debug(message: types.Message):
    print("CHAT ID:", message.chat.id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

