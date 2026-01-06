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
# user_id: {"step": "...", "car": str}

# ================== ТЕКСТЫ ==================
TEXT = {
    "welcome": (
        "👋 Добро пожаловать в Prime Fusion!\n\n"
        "• Если вы *новый клиент* — пройдите анкету\n"
        "• Если хотите *разместить свои автомобили на сайте* — свяжитесь с нами через контакты"
    ),
    "contacts": (
        "📞 Контакты для сотрудничества и размещения авто:\n\n"
        "Telegram: @primefusion_admin\n"
        "Email: info@primefusioncars.com"
    ),
    "fail": "❌ К сожалению, на данный момент сервис вам не подходит.",
    "success": (
        "✅ Вы подходите под условия.\n\n"
        "Перейдите на сайт для получения полной информации и бронирования."
    )
}

# ================== КЛАВИАТУРЫ ==================
def menu_new_user_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Анкета", callback_data="menu:form")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="menu:contacts")]
    ])

def menu_allowed_user_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧰 Рабочее меню", callback_data="menu:work")]
    ])

def yes_no_kb(step: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data=f"{step}:yes"),
            InlineKeyboardButton(text="❌ Нет", callback_data=f"{step}:no")
        ]
    ])

def site_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚗 Перейти на сайт",
            web_app=WebAppInfo(url=SITE_URL)
        )]
    ])

def bottom_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 В главное меню")]],
        resize_keyboard=True
    )

# ================== START ==================
@dp.message(CommandStart())
async def start(message: types.Message):
    uid = message.from_user.id
    TEMP.pop(uid, None)

    if uid in ALLOWED_DRIVERS:
        await message.answer(
            "👋 Добро пожаловать в Prime Fusion!\n\n"
            "Вы находитесь в рабочем пространстве арендодатора.\n"
            "Используйте рабочее меню для связи с администрацией.",
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            "🧰 Рабочее меню 👇",
            reply_markup=menu_allowed_user_kb()
        )
    else:
        await message.answer(
            "👋 Добро пожаловать в Prime Fusion!\n\n"
            "• Если вы *новый клиент* — пройдите анкету\n"
            "• Если хотите *разместить свои автомобили на сайте* — "
            "свяжитесь с нами через контакты",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            "Выберите действие 👇",
            reply_markup=menu_new_user_kb()
        )


# ================== ВОЗВРАТ В МЕНЮ ==================
@dp.message(lambda m: m.text == "🔄 В главное меню")
async def back_to_menu(message: types.Message):
    await start(message)

# ================== КОНТАКТЫ ==================
@dp.callback_query(lambda c: c.data == "menu:contacts")
async def menu_contacts(callback: types.CallbackQuery):
    await callback.message.edit_text(TEXT["contacts"])

# ================== АНКЕТА ==================
@dp.callback_query(lambda c: c.data == "menu:form")
async def form_start(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Есть ли у вас TLC-лицензия?",
        reply_markup=yes_no_kb("tlc")
    )

@dp.callback_query(lambda c: c.data.startswith("tlc"))
async def q_tlc(callback: types.CallbackQuery):
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT["fail"])
        return
    await callback.message.edit_text(
        "Стаж вождения в США 1+ год?",
        reply_markup=yes_no_kb("exp")
    )

@dp.callback_query(lambda c: c.data.startswith("exp"))
async def q_exp(callback: types.CallbackQuery):
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT["fail"])
        return
    await callback.message.edit_text(
        "Вы ищете автомобиль в аренду?",
        reply_markup=yes_no_kb("rent")
    )

@dp.callback_query(lambda c: c.data.startswith("rent"))
async def q_rent(callback: types.CallbackQuery):
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT["fail"])
        return
    await callback.message.edit_text(
        "Подходит ли Toyota Sienna Hybrid (VAN)?",
        reply_markup=yes_no_kb("car")
    )

@dp.callback_query(lambda c: c.data.startswith("car"))
async def q_car(callback: types.CallbackQuery):
    if callback.data.endswith("no"):
        await callback.message.edit_text(TEXT["fail"])
        return
    await callback.message.edit_text(
        TEXT["success"],
        reply_markup=site_kb()
    )

# ================== РАБОЧЕЕ МЕНЮ ==================
@dp.callback_query(lambda c: c.data == "menu:work")
async def work_menu(callback: types.CallbackQuery):
    uid = callback.from_user.id
    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text("⛔️ У вас нет доступа.")
        return

    TEMP[uid] = {"step": "car"}
    await callback.message.edit_text("🚗 Введите номер автомобиля:")
    await callback.message.answer(
        "Вы можете вернуться в меню 👇",
        reply_markup=bottom_menu_kb()
    )

# ================== СООБЩЕНИЯ ВОДИТЕЛЕЙ ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id
    if uid not in TEMP:
        return

    if TEMP[uid]["step"] == "car":
        TEMP[uid]["car"] = message.text.strip()
        TEMP[uid]["step"] = "msg"
        await message.answer("✍️ Напишите сообщение администрации:")
        return

    if TEMP[uid]["step"] == "msg":
        text = (
            "🚗 Сообщение от арендодатора\n\n"
            f"Авто: {TEMP[uid]['car']}\n"
            f"ID: {uid}\n"
            f"Username: @{message.from_user.username or 'нет'}\n\n"
            f"Сообщение:\n{message.text}"
        )

        await bot.send_message(CHANNEL_ID, text)

        await message.answer(
            "✅ Сообщение отправлено.\n"
            "Можете написать ещё или вернуться в меню 👇",
            reply_markup=bottom_menu_kb()
        )

# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



