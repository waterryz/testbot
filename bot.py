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

ALLOWED_DRIVERS = {5348697217, 222222222}

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== ВРЕМЕННОЕ СОСТОЯНИЕ ==================
TEMP = {}
# user_id: {"step": "name", "name": str}

# ================== КНОПКИ ==================
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆕 Новый арендатор", callback_data="role:new")],
        [InlineKeyboardButton(text="🚗 Действующий водитель", callback_data="role:active")]
    ])

def bottom_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔄 В главное меню")]
        ],
        resize_keyboard=True
    )

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    TEMP.pop(message.from_user.id, None)
    await message.answer(
        "Выберите действие:",
        reply_markup=main_menu_kb()
    )

# ================== КНОПКА СНИЗУ ==================
@dp.message(lambda m: m.text == "🔄 В главное меню")
async def go_main_menu(message: types.Message):
    TEMP.pop(message.from_user.id, None)
    await message.answer(
        "Выберите действие:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb()
    )

# ================== НОВЫЙ АРЕНДАТОР ==================
@dp.callback_query(lambda c: c.data == "role:new")
async def new_renter(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📝 Для аренды автомобиля перейдите на сайт:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🚗 Перейти на сайт",
                web_app=WebAppInfo(url=SITE_URL)
            )]
        ])
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

# ================== СООБЩЕНИЯ ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id

    if uid not in TEMP:
        return

    # Шаг 1 — имя
    if TEMP[uid]["step"] == "name":
        TEMP[uid]["name"] = message.text.strip()
        TEMP[uid]["step"] = "msg"

        await message.answer(
            "✍️ Теперь напишите сообщение по работе:"
        )
        return

    # Шаг 2 — сообщение
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

        TEMP[uid]["step"] = "msg"  # можно писать ещё
