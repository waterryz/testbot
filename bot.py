import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8550400671:AAHZdPJcWi_NtkurCHGxUgmRsQKMTu3826g"
CHANNEL_ID = -1003580316890 
SITE_URL = "https://www.primefusioncars.com/" =
ALLOWED_DRIVERS = { 5348697217, 222222222, }

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== ХРАНИЛИЩЕ ПРОФИЛЕЙ ==================
DRIVERS = {}  
# user_id: {"username": str}

# ================== КНОПКИ ==================
def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])

def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆕 Новый арендатор", callback_data="role:new")],
        [InlineKeyboardButton(text="🚗 Действующий водитель", callback_data="role:active")]
    ])

def driver_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Профиль", callback_data="driver:profile")],
        [InlineKeyboardButton(text="💬 Сообщение по работе", callback_data="driver:msg")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="driver:settings")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Выберите, кто вы:", reply_markup=main_menu_kb())

# ================== НАЗАД ==================
@dp.callback_query(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите, кто вы:", reply_markup=main_menu_kb())

# ================== ДЕЙСТВУЮЩИЙ ВОДИТЕЛЬ ==================
@dp.callback_query(lambda c: c.data == "role:active")
async def role_active(callback: types.CallbackQuery):
    uid = callback.from_user.id

    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text("⛔️ Доступ запрещён")
        return

    if uid not in DRIVERS:
        await callback.message.edit_text(
            "Введите ваш username (без @):",
            reply_markup=back_kb()
        )
        return

    await callback.message.edit_text(
        "Меню водителя:",
        reply_markup=driver_menu_kb()
    )

# ================== СОХРАНЕНИЕ USERNAME ==================
@dp.message()
async def save_username_or_message(message: types.Message):
    uid = message.from_user.id

    # если водитель авторизован и ещё нет профиля
    if uid in ALLOWED_DRIVERS and uid not in DRIVERS:
        username = message.text.strip().lstrip("@")
        DRIVERS[uid] = {"username": username}

        await message.answer(
            "✅ Профиль сохранён",
            reply_markup=driver_menu_kb()
        )
        return

    # ================== СООБЩЕНИЯ ПО РАБОТЕ ==================
    if uid in DRIVERS and getattr(message, "send_work", False):
        text = (
            "🚗 Сообщение от водителя\n\n"
            f"👤 @{DRIVERS[uid]['username']}\n"
            f"🆔 {uid}\n\n"
            f"💬 {message.text}"
        )
        await bot.send_message(CHANNEL_ID, text)
        await message.answer("✅ Отправлено")
        return

# ================== ПРОФИЛЬ ==================
@dp.callback_query(lambda c: c.data == "driver:profile")
async def profile(callback: types.CallbackQuery):
    uid = callback.from_user.id
    profile = DRIVERS.get(uid)

    await callback.message.edit_text(
        f"👤 Профиль\n\n"
        f"Username: @{profile['username']}\n"
        f"ID: {uid}",
        reply_markup=driver_menu_kb()
    )

# ================== СООБЩЕНИЕ ПО РАБОТЕ ==================
@dp.callback_query(lambda c: c.data == "driver:msg")
async def work_message(callback: types.CallbackQuery):
    uid = callback.from_user.id

    await callback.message.edit_text(
        "✍️ Напишите сообщение по работе:",
        reply_markup=back_kb()
    )

    # флаг
    callback.message.send_work = True

# ================== НАСТРОЙКИ ==================
@dp.callback_query(lambda c: c.data == "driver:settings")
async def settings(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "⚙️ Настройки\n\n(пока пусто)",
        reply_markup=driver_menu_kb()
    )

# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
