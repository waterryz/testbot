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

# ================== ВРЕМЕННОЕ СОСТОЯНИЕ ==================
TEMP = {}
# user_id: {"step": "...", "name": str}

# ================== ТЕКСТЫ АНКЕТЫ ==================
TEXT = {
    "welcome": "Ответьте на несколько вопросов:",
    "tlc": "Есть ли у вас TLC-лицензия?",
    "exp": "Стаж вождения в США 1+ год?",
    "rent": "Вы ищете автомобиль в аренду?",
    "car": "Подходит ли Toyota Sienna Hybrid (VAN)?",
    "fail": "К сожалению, на данный момент сервис вам не подходит.",
    "success": (
        "✅ Вы подходите под условия.\n\n"
        "Перейдите на сайт для получения полной информации и бронирования."
    ),
    "site": "🚗 Перейти на сайт"
}

# ================== КНОПКИ ==================
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆕 Новый арендатор", callback_data="role:new")],
        [InlineKeyboardButton(text="🚗 Действующий водитель", callback_data="role:active")]
    ])

def bottom_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 В главное меню")]],
        resize_keyboard=True
    )

def yes_no_kb(step: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data=f"{step}:yes"),
            InlineKeyboardButton(text="❌ Нет", callback_data=f"{step}:no"),
        ]
    ])

def site_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=TEXT["site"],
            web_app=WebAppInfo(url=SITE_URL)
        )]
    ])

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    TEMP.pop(message.from_user.id, None)
    await message.answer(
        "Выберите действие:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb()
    )

# ================== КНОПКА СНИЗУ ==================
@dp.message(lambda m: m.text == "🔄 В главное меню")
async def go_main_menu(message: types.Message):
    TEMP.pop(message.from_user.id, None)
    await message.answer(
        "Главное меню:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Выберите действие:",
        reply_markup=main_menu_kb()
    )

# ================== НОВЫЙ АРЕНДАТОР (АНКЕТА) ==================
@dp.callback_query(lambda c: c.data == "role:new")
async def new_renter(callback: types.CallbackQuery):
    await callback.message.edit_text(
        TEXT["welcome"],
        reply_markup=yes_no_kb("tlc")
    )

@dp.callback_query(lambda c: c.data.startswith("tlc"))
async def q_tlc(callback: types.CallbackQuery):
    _, answer = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT["fail"])
        return
    await callback.message.edit_text(TEXT["exp"], reply_markup=yes_no_kb("exp"))

@dp.callback_query(lambda c: c.data.startswith("exp"))
async def q_exp(callback: types.CallbackQuery):
    _, answer = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT["fail"])
        return
    await callback.message.edit_text(TEXT["rent"], reply_markup=yes_no_kb("rent"))

@dp.callback_query(lambda c: c.data.startswith("rent"))
async def q_rent(callback: types.CallbackQuery):
    _, answer = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT["fail"])
        return
    await callback.message.edit_text(TEXT["car"], reply_markup=yes_no_kb("car"))

@dp.callback_query(lambda c: c.data.startswith("car"))
async def q_car(callback: types.CallbackQuery):
    _, answer = callback.data.split(":")
    if answer == "no":
        await callback.message.edit_text(TEXT["fail"])
        return

    await callback.message.edit_text(
        TEXT["success"],
        reply_markup=site_kb()
    )

# ================== ДЕЙСТВУЮЩИЙ ВОДИТЕЛЬ ==================
@dp.callback_query(lambda c: c.data == "role:active")
async def active_driver(callback: types.CallbackQuery):
    uid = callback.from_user.id

    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text(
            "⛔️ У вас нет доступа.\nОбратитесь к администрации."
        )
        return

    TEMP[uid] = {"step": "name"}

    await callback.message.edit_text(
        "Введите ваше **Имя и Фамилию**:"
    )
    await callback.message.answer(
        "Вы можете в любой момент вернуться в меню 👇",
        reply_markup=bottom_menu_kb()
    )

# ================== СООБЩЕНИЯ ОТ ВОДИТЕЛЕЙ ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id

    if uid not in TEMP:
        return

    # шаг 1 — имя
    if TEMP[uid]["step"] == "name":
        TEMP[uid]["name"] = message.text.strip()
        TEMP[uid]["step"] = "msg"
        await message.answer("✍️ Теперь напишите сообщение по работе:")
        return

    # шаг 2 — сообщение
    if TEMP[uid]["step"] == "msg":
        text = (
            "🚗 Сообщение от водителя\n\n"
            f"👤 {TEMP[uid]['name']}\n"
            f"🆔 {uid}\n"
            f"🔗 @{message.from_user.username or 'без username'}\n\n"
            f"💬 {message.text}"
        )

        await bot.send_message(CHANNEL_ID, text)

        await message.answer(
            "✅ Сообщение отправлено администрации.\n"
            "Можете отправить ещё одно или вернуться в меню 👇",
            reply_markup=bottom_menu_kb()
        )

        TEMP[uid]["step"] = "msg"

# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


