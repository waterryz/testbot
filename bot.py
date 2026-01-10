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

ALLOWED_DRIVERS = {5348697217, 5470043640}

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== TEMP ==================
TEMP = {}
# user_id: {"lang":"ru/en", "step":"...", "car":str, "text":str}

# ================== ТЕКСТЫ ==================
TEXT = {
    "ru": {
        "choose_lang": "🌐 Выберите язык / Choose language",
        "work_info": (
            "🛠 *Обслуживание автомобиля*\n\n"
            "*Основной сервис и контакты:*\n\n"
            "🔧 *Игорь Электрик* — +1 (646) 420–7572\n"
            "📍 2029 E 24th St, Brooklyn, NY\n"
            "Мелкий ремонт и электрика.\n"
            "Работает у себя дома после 10:00, нужна запись.\n\n"
            "🚗 *K, R & S Auto Service*\n"
            "📍 2965 86th Street, Brooklyn, NY 11223\n"
            "📞 (718) 891–6626\n"
            "Без записи, лучше приезжать к открытию.\n"
            "Менеджеры Алекс и Гарри говорят по-русски.\n"
            "Без выходных.\n\n"
            "💰 *Оплата сервиса*\n"
            "Платить за сервис не нужно — это включено в аренду.\n"
            "Оплату счетов веду я.\n\n"
            "*Регулярное ТО:*\n"
            "• Замена масла каждые 7000 миль\n"
            "• Только full synthetic (Toyota / Mobil 1)\n"
            "  до 50k — 0W16\n"
            "  50k–150k — 0W20\n"
            "  150k+ — 5W30\n\n"
            "📸 *Фото ресита обязательно:*\n"
            "дата, номер авто, список работ, марка масла, цена.\n"
            "На СТО часто забывают писать марку масла — проверяйте.\n\n"
            "*Фильтры гибридной батареи:*\n"
            "• Менять раз в 6 месяцев\n"
            "• Фильтры выдаю я, в сервисе их нет\n"
            "• Фото после обслуживания обязательно\n\n"
            "*Дополнительно:*\n"
            "• Каждую 2-ю замену масла — фильтры салона и двигателя\n"
            "• Каждую замену масла — ротация колёс\n"
            "• Давление в шинах: 35 psi\n"
            "• Износ шин — ответственность арендатора\n\n"
            "📸 После каждого ТО отправляйте в WhatsApp:\n"
            "• фото одометра\n\n"
            "*DMV-инспекция:*\n"
            "Проходит раз в 4 месяца — ответственность арендатора.\n"
            "Uber напоминает, Lyft — нет.\n"
            "Просрочка → штраф $200 (платит арендатор).\n"
            "В день инспекции — фото авто с 4 сторон.\n\n"
            "*Повреждения:*\n"
            "Не скрывайте повреждения.\n"
            "Если не мешают работе — можно сделать эстимейт,\n"
            "согласовать сумму и перевести мне.\n\n"
            "*Компенсация простоя:*\n"
            "Плановое ТО не компенсируется.\n"
            "Поломка → 1 бесплатный день аренды,\n"
            "если простой > 4 часов.\n\n"
            "*Скрип дверей после дождя:*\n"
            "Использовать WD-40 в щели под окном 3-го ряда.\n"
            "Несколько раз открыть/закрыть дверь.\n\n"
            "*Батарейка брелка:*\n"
            "Меняйте вовремя — разряженный брелок\n"
            "может не сработать в критический момент."
         ),


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
            "Email: info@primefusioncars.com\n"
            "Администратор: @wateryz"
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
            "📸 Фото обязательно.\n"
            "✍️ После фото потребуется комментарий."
        ),
        "work_info": (
            "🛠 *Vehicle Maintenance*\n\n"
            "*Main service & contacts:*\n\n"
            "🔧 *Igor Electrician* — +1 (646) 420–7572\n"
            "📍 2029 E 24th St, Brooklyn, NY\n"
            "Minor repairs & electrical work.\n"
            "Works after 10:00 AM, appointment required.\n\n"
            "🚗 *K, R & S Auto Service*\n"
            "📍 2965 86th Street, Brooklyn, NY 11223\n"
            "📞 (718) 891–6626\n"
            "No appointment needed, arrive early.\n"
            "Managers Alex & Harry speak Russian.\n"
            "Open daily.\n\n"
            "💰 *Service payment*\n"
            "Service is included in rental price.\n"
            "I handle all payments.\n\n"
            "*Regular maintenance:*\n"
            "• Oil change every 7000 miles\n"
            "• Full synthetic only (Toyota / Mobil 1)\n"
            "  up to 50k — 0W16\n"
            "  50k–150k — 0W20\n"
            "  150k+ — 5W30\n\n"
            "📸 *Receipt photo required:*\n"
            "date, car number, work list, oil brand, price.\n\n"
            "*Hybrid battery filters:*\n"
            "• Replace every 6 months\n"
            "• Filters provided by me\n"
            "• Photo after service required\n\n"
            "*Additional:*\n"
            "• Every 2nd oil change — cabin & engine filters\n"
            "• Every oil change — tire rotation\n"
            "• Tire pressure: 35 psi\n"
            "• Tire wear is tenant responsibility\n\n"
            "📸 After service send to WhatsApp:\n"
            "• odometer photo\n\n"
            "*DMV inspection:*\n"
            "Required every 4 months.\n"
            "Uber reminds, Lyft does not.\n"
            "Late → $200 fine (tenant pays).\n"
            "Inspection day — photos from all 4 sides.\n\n"
            "*Downtime compensation:*\n"
            "Planned service is not compensated.\n"
            "Breakdown → 1 free rental day\n"
            "if downtime exceeds 4 hours.\n\n"
            "*Door squeak after rain:*\n"
            "Apply WD-40 under 3rd row window seal.\n\n"
            "*Key fob battery:*\n"
            "Replace on time — dead battery may fail\n"
            "in a critical moment."
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
            "Email: info@primefusioncars.com\n"
            "Administrator: @wateryz"
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
            "📸 Photo is required.\n"
            "✍️ Comment after photo."
        ),


        "ask_car": "🚗 Enter vehicle number:",
        "ask_text": "✍️ Enter message:",
        "ask_photo": "📸 Upload photo.",
        "sent": "✅ Message sent.",
        "no_access": "⛔️ No access."
    }
}

# ================== КЛАВИАТУРЫ ==================
def work_menu_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🧾 DMV инспекция" if lang=="ru" else "🧾 DMV inspection",
            callback_data="work:dmv"
        )],
        [InlineKeyboardButton(
            text="🛠 Сервис" if lang=="ru" else "🛠 Service",
            callback_data="work:service"
        )],
        [InlineKeyboardButton(
            text="ℹ️ Информация" if lang=="ru" else "ℹ️ Information",
            callback_data="work:info"
        )],
        [InlineKeyboardButton(
            text="📞 Связаться с администратором" if lang=="ru" else "📞 Contact admin",
            callback_data="work:admin"
        )],
    ])


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

    TEMP[uid].pop("step", None)
    await callback.message.edit_text(
        TEXT[lang]["work_intro"],
        reply_markup=work_menu_kb(lang)
    )
@dp.callback_query(lambda c: c.data.startswith("work:"))
async def work_start(callback: types.CallbackQuery):
    uid = callback.from_user.id
    lang = get_lang(uid)

    if uid not in ALLOWED_DRIVERS:
        await callback.message.edit_text(TEXT[lang]["no_access"])
        return

    action = callback.data.split(":")[1]

    # 📞 Связь с администратором
    if action == "admin":
        await callback.message.edit_text(TEXT[lang]["contacts"])
        return

    # 🧾 DMV или 🛠 Service
    TEMP[uid]["work_type"] = action
    TEMP[uid]["step"] = "work_car"

    await callback.message.edit_text(
        "🚗 Введите номер автомобиля:"
        if lang == "ru" else
        "🚗 Enter vehicle number:"
    )



# ================== HANDLE MESSAGES ==================
@dp.message()
async def handle_messages(message: types.Message):
    uid = message.from_user.id
    if uid not in TEMP:
        return

    lang = get_lang(uid)
    step = TEMP[uid].get("step")

    # ================== CONSULT ==================
    if step == "consult":
        await bot.send_message(
            CHANNEL_ID,
            f"💼 Consultation\n"
            f"ID: {uid}\n"
            f"@{message.from_user.username or 'no_username'}\n\n"
            f"{message.text}"
        )
        TEMP[uid]["step"] = None
        await message.answer(
            TEXT[lang]["consult_done"],
            reply_markup=bottom_menu_kb(lang)
        )
        return

    # ================== ACCESS CHECK ==================
    if uid not in ALLOWED_DRIVERS:
        return

    # ================== WORK CAR ==================
    if step == "work_car":
        car = message.text.strip()
        if not car:
            await message.answer(
                "❗️Введите номер автомобиля."
                if lang == "ru" else
                "❗️Please enter vehicle number.",
                reply_markup=bottom_menu_kb(lang)
            )
            return

        TEMP[uid]["car"] = car
        TEMP[uid]["step"] = "work_photo"

        await message.answer(
            "📸 Скиньте фото DMV-инспекции"
            if TEMP[uid]["work_type"] == "dmv" and lang == "ru" else
            "📸 Send DMV inspection photo"
            if TEMP[uid]["work_type"] == "dmv" else
            "📸 Скиньте фото сервиса"
            if lang == "ru" else
            "📸 Send service photo"
        )
        return

    # ================== WORK PHOTO (REQUIRED) ==================
    if step == "work_photo":
        if not (
            message.photo or
            (message.document and (message.document.mime_type or "").startswith("image/"))
        ):
            await message.answer(
                "❗️Фото обязательно. Без фото отправка невозможна."
                if lang == "ru" else
                "❗️Photo is required. Submission without photo is not allowed.",
                reply_markup=bottom_menu_kb(lang)
            )
            return

        TEMP[uid]["photo"] = (
            message.photo[-1].file_id
            if message.photo else
            message.document.file_id
        )
        TEMP[uid]["step"] = "work_comment"

        await message.answer(
            "✍️ Комментарий к DMV-инспекции:"
            if TEMP[uid]["work_type"] == "dmv" and lang == "ru" else
            "✍️ Comment for DMV inspection:"
            if TEMP[uid]["work_type"] == "dmv" else
            "✍️ Комментарий к сервису:"
            if lang == "ru" else
            "✍️ Comment for service:"
        )
        return

    # ================== WORK COMMENT ==================
    if step == "work_comment":
        # защита от битой сессии
        if "work_type" not in TEMP[uid] or "photo" not in TEMP[uid] or "car" not in TEMP[uid]:
            TEMP[uid].pop("step", None)
            await message.answer(
                "⚠️ Сессия устарела. Начните заново."
                if lang == "ru" else
                "⚠️ Session expired. Please start again.",
                reply_markup=bottom_menu_kb(lang)
            )
            return

        caption = (
            f"🛠 {TEMP[uid]['work_type'].upper()}\n"
            f"🚗 Car: {TEMP[uid]['car']}\n"
            f"ID: {uid}\n"
            f"@{message.from_user.username or 'no_username'}\n\n"
            f"{message.text}"
        )

        await bot.send_photo(
            CHANNEL_ID,
            TEMP[uid]["photo"],
            caption=caption
        )

        # очищаем состояние (язык сохраняем)
        TEMP[uid].pop("step", None)
        TEMP[uid].pop("work_type", None)
        TEMP[uid].pop("photo", None)
        TEMP[uid].pop("car", None)

        await message.answer(
            TEXT[lang]["sent"],
            reply_markup=bottom_menu_kb(lang)
        )
        return





# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())









