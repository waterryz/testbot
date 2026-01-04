import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8550400671:AAHZdPJcWi_NtkurCHGxUgmRsQKMTu3826g"
CHANNEL_ID = -1003580316890
SITE_URL = "https://www.primefusioncars.com/"

ALLOWED_DRIVERS = {5348697217, 222222222}

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== ВРЕМЕННЫЕ ДАННЫЕ ==================
TEMP = {}  # user_id: {"step": "name"}

# ================== КНОПКИ ==================
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆕 Новый арендатор", callback_data="role:new")],
        [InlineKeyboardButton(text="🚗 Действующий водитель", callback_data="role:active")]
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])

def restart_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Запустить бота", callback_data="restart")]
    ])

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=main_menu_kb()
    )

# ================== RESTART ==================
@dp.callback_query(lambda c: c.data in ("restart", "back"))
async def restart(callback: types.CallbackQuery):
    TEMP.pop(callback.from_user.id, None)
    await callback.message.edit_text(
        "Выберите действие:",
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
            )],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ])
    )

# ================== ДЕЙСТВУЮЩИЙ ВОДИТЕЛЬ ==================
@dp.callback_query(lambda c: c.data == "role:active")
async def active_driver(callback: types.CallbackQuery):
    uid = callback.from_user.id

    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text(
            "⛔️ У вас нет доступа.\n"
            "Обратитесь к администрации.",
            reply_markup=restart_kb()
        )
        return

    TEMP[uid] = {"step": "name"}
    await callback.message.edit_text(
        "Введите ваше **Имя и Фамилию**:",
        reply_markup=back_kb()
    )

# ================== СООБЩЕНИЯ ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id

    if uid not in TEMP:
        return

    # шаг 1 — имя
    if TEMP[uid]["step"] == "name":
        TEMP[uid]["name"] = message.text.strip()
        TEMP[uid]["step"] = "msg"

        await message.answer(
            "✍️ Теперь напишите сообщение по работе:",
            reply_markup=back_kb()
        )
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
            "✅ Сообщение отправлено администрации",
            reply_markup=restart_kb()
        )

        TEMP.pop(uid, None)

# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
