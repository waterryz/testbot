import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8550400671:AAHZdPJcWi_NtkurCHGxUgmRsQKMTu3826g"
CHANNEL_ID = -1003580316890

ALLOWED_DRIVERS = {
    5348697217,
    222222222,
}

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== ВРЕМЕННОЕ ХРАНИЛИЩЕ ==================
TEMP = {}
# user_id: {"name": str}

# ================== КНОПКИ ==================
def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])

def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Действующий водитель", callback_data="role:active")]
    ])

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=main_menu_kb()
    )

# ================== НАЗАД ==================
@dp.callback_query(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    TEMP.pop(callback.from_user.id, None)
    await callback.message.edit_text(
        "Выберите действие:",
        reply_markup=main_menu_kb()
    )

# ================== ДЕЙСТВУЮЩИЙ ВОДИТЕЛЬ ==================
@dp.callback_query(lambda c: c.data == "role:active")
async def role_active(callback: types.CallbackQuery):
    uid = callback.from_user.id

    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text("⛔️ У вас нет доступа")
        return

    TEMP[uid] = {}
    await callback.message.edit_text(
        "Введите ваше **Имя и Фамилию**:",
        reply_markup=back_kb()
    )

# ================== СООБЩЕНИЯ ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id

    if uid not in ALLOWED_DRIVERS:
        return

    # 1️⃣ Имя и фамилия
    if uid in TEMP and "name" not in TEMP[uid]:
        TEMP[uid]["name"] = message.text.strip()
        await message.answer(
            "✍️ Теперь напишите сообщение по работе:",
            reply_markup=back_kb()
        )
        return

    # 2️⃣ Сообщение по работе
    if uid in TEMP and "name" in TEMP[uid]:
        text = (
            "🚗 Сообщение от водителя\n\n"
            f"👤 {TEMP[uid]['name']}\n"
            f"🆔 {uid}\n"
            f"🔗 @{message.from_user.username or 'без username'}\n\n"
            f"💬 {message.text}"
        )

        await bot.send_message(CHANNEL_ID, text)
        await message.answer("✅ Сообщение отправлено администрации")

        TEMP.pop(uid, None)
        return

# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
