import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8550400671:AAHZdPJcWi_NtkurCHGxUgmRsQKMTu3826g"
SITE_URL = "https://www.primefusioncars.com/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== ТЕКСТЫ =====
TEXT = {
    "ru": {
        "start": "Выберите язык:",
        "welcome": "Проверим, подходите ли вы для аренды авто.",
        "tlc": "У вас есть TLC-лицензия?",
        "exp": "Стаж вождения в США 1+ год?",
        "rent": "Вы ищете автомобиль в аренду?",
        "car": "Вам подходит Toyota Sienna Hybrid (VAW)?",
        "fail": "К сожалению, вы не подходите под условия.",
        "success": "✅ Вы подходите!\n\nПерейдите на сайт для бронирования.",
        "site": "🚗 Перейти на сайт"
    },
    "en": {
        "start": "Choose language:",
        "welcome": "Let’s check if you qualify for renting a vehicle.",
        "tlc": "Do you have a TLC license?",
        "exp": "Do you have 1+ year driving experience in the USA?",
        "rent": "Are you looking for a rental car?",
        "car": "Is Toyota Sienna Hybrid (VAW) suitable for you?",
        "fail": "Sorry, you do not meet the requirements.",
        "success": "✅ You qualify!\n\nGo to the website for booking.",
        "site": "🚗 Go to website"
    }
}

# ===== КНОПКИ =====
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
        [
            InlineKeyboardButton(
                text=TEXT[lang]["site"],
                web_app=WebAppInfo(url=SITE_URL)
            )
        ]
    ])

# ===== START =====
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Choose language / Выберите язык:", reply_markup=lang_kb())

# ===== LANGUAGE =====
@dp.callback_query(lambda c: c.data.startswith("lang"))
async def choose_lang(callback: types.CallbackQuery):
    lang = callback.data.split(":")[1]
    await callback.message.edit_text(
        TEXT[lang]["welcome"],
        reply_markup=yes_no_kb("tlc", lang)
    )

# ===== ВОПРОСЫ =====
@dp.callback_query(lambda c: c.data.startswith("tlc"))
async def q_tlc(callback: types.CallbackQuery):
    _, answer, lang = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        TEXT[lang]["exp"],
        reply_markup=yes_no_kb("exp", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("exp"))
async def q_exp(callback: types.CallbackQuery):
    _, answer, lang = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        TEXT[lang]["rent"],
        reply_markup=yes_no_kb("rent", lang)
    )

@dp.callback_query(lambda c: c.data.startswith("rent"))
async def q_rent(callback: types.CallbackQuery):
    _, answer, lang = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT[lang]["fail"])
        return
    await callback.message.edit_text(
        TEXT[lang]["car"],
        reply_markup=yes_no_kb("car", lang)
    )

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

# ===== RUN =====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

