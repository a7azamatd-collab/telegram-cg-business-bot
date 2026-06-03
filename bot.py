import asyncio
from dotenv import load_dotenv
load_dotenv()
import os
from openai import AsyncOpenAI
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile,
    ReplyKeyboardRemove
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = os.getenv("BOT_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_ai = AsyncOpenAI(
    api_key=OPENAI_API_KEY
)

user_history = {}

ADMIN_ID = 490936540

bot = Bot(token=TOKEN)
dp = Dispatcher()

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials_path = "/etc/secrets/credentials.json"
if not os.path.exists(credentials_path):
    credentials_path = "credentials.json"

creds = ServiceAccountCredentials.from_json_keyfile_name(
    credentials_path,
    scope
)

client = gspread.authorize(creds)

sheet = client.open("CRM Заявки").sheet1

class RequestForm(StatesGroup):
    name = State()
    phone = State()
    comment = State()

class AIChat(StatesGroup):
    chat = State()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🤖 AI Консультант",
                callback_data="ai_consultant"
            )
        ],
        [
            InlineKeyboardButton(
                text="💼 Каталог решений",
                callback_data="catalog"
            )
        ],
        [
            InlineKeyboardButton(
                text="📞 Контакты",
                callback_data="contacts"
            )
        ],
        [
            InlineKeyboardButton(
                text="🖼 Портфолио",
                callback_data="portfolio"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Оставить заявку",
                callback_data="request"
            )
        ]
    ]
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Выберите нужный раздел:",
        reply_markup=keyboard
    )
@dp.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):

    catalog_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔹 Бот-визитка", callback_data="card_bot")],
            [InlineKeyboardButton(text="🔹 Бизнес-бот", callback_data="business_bot")],
            [InlineKeyboardButton(text="🔹 Магазин-бот", callback_data="shop_bot")],
            [InlineKeyboardButton(text="🤖 AI / ChatGPT бот", callback_data="ai_bot")],
            [InlineKeyboardButton(text="⚙ Индивидуальная разработка", callback_data="custom_bot")]
        ]
    )
    await callback.message.answer(
        "🗂 Выберите интересующий вас тариф:",
        reply_markup=catalog_keyboard
    )
    await callback.answer()

TARIF_DETAILS = {
"card_bot": {
    "photo": "tarif/visitka.png",
    "caption": (
        "━━━━━━━━━━━━━━━\n"
        "🔹 БОТ-ВИЗИТКА\n\n"
        "💰 Стоимость\n"
        "от 70 000 ₸\n\n"
        "🔄 Поддержка\n"
        "40 000 ₸ / месяц\n\n"
        "🎯 Подходит для\n"
        "• Мастеров\n"
        "• Услуг\n"
        "• Небольших компаний\n\n"
        "📦 Что входит\n\n"
        "✅ Красивое меню\n"
        "✅ Контакты\n"
        "✅ FAQ\n"
        "✅ Сбор заявок\n"
        "✅ CRM Google Sheets\n"
        "✅ Работа 24/7\n\n"
        "⏳ Срок разработки\n"
        "3–7 дня\n"
        "━━━━━━━━━━━━━━━"
    ),
    "tariff_name": "Бот-визитка"
},
"business_bot": {
    "photo": "tarif/business.png",
    "caption": (
        "━━━━━━━━━━━━━━━\n"
        "🔹 БИЗНЕС-БОТ\n\n"
        "💰 Стоимость\n"
        "от 150 000 ₸\n\n"
        "🔄 Поддержка\n"
        "70 000 ₸ / месяц\n\n"
        "🎯 Подходит для\n"
        "• Салонов красоты\n"
        "• Автосервисов\n"
        "• Мебельных компаний\n"
        "• Доставки\n\n"
        "📦 Что входит\n\n"
        "✅ Каталог услуг\n"
        "✅ Фото и карточки\n"
        "✅ CRM клиентов\n"
        "✅ Уведомления админу\n"
        "✅ Рассылки\n"
        "✅ Работа 24/7\n\n"
        "⏳ Срок разработки\n"
        "7–10 дней\n"
        "━━━━━━━━━━━━━━━"
    ),
    "tariff_name": "Бизнес-бот"
},
"shop_bot": {
    "photo": "tarif/shop.png",
    "caption": (
        "━━━━━━━━━━━━━━━\n"
        "🛍 МАГАЗИН-БОТ\n\n"
        "💰 Стоимость\n"
        "от 150 000 ₸\n\n"
        "🔄 Поддержка\n"
        "90 000 ₸ / месяц\n\n"
        "📦 Что входит\n\n"
        "✅ Каталог товаров\n"
        "✅ Фото товаров\n"
        "✅ Категории\n"
        "✅ Корзина\n"
        "✅ Заказы\n"
        "✅ CRM клиентов\n"
        "✅ Админ-панель\n"
        "✅ Работа 24/7\n\n"
        "⏳ Срок разработки\n"
        "7–20 дней\n"
        "━━━━━━━━━━━━━━━"
    ),
    "tariff_name": "Магазин-бот"
},
"ai_bot": {
    "photo": "tarif/ai.png",
    "caption": (
        "━━━━━━━━━━━━━━━\n"
        "🤖 AI / CHATGPT БОТ\n\n"
        "💰 Стоимость\n"
        "от 300 000 ₸\n\n"
        "🔄 Поддержка\n"
        "150 000 ₸ / месяц\n\n"
        "📦 Что входит\n\n"
        "✅ AI-консультант\n"
        "✅ ChatGPT интеграция\n"
        "✅ Ответы клиентам 24/7\n"
        "✅ Автоматизация продаж\n"
        "✅ CRM интеграции\n"
        "✅ Индивидуальное обучение\n\n"
        "⏳ Срок разработки\n"
        "7–20 дней\n"
        "━━━━━━━━━━━━━━━"
    ),
    "tariff_name": "AI / ChatGPT бот"
},
"custom_bot": {
    "photo": "tarif/custom.png",
    "caption": (
        "━━━━━━━━━━━━━━━\n"
        "⚙ ИНДИВИДУАЛЬНАЯ РАЗРАБОТКА\n\n"
        "💰 Стоимость\n"
        "от 500 000 ₸\n\n"
        "📦 Возможности\n\n"
        "✅ Telegram Mini App\n"
        "✅ Онлайн-оплата\n"
        "✅ CRM интеграции\n"
        "✅ Автоматизация бизнеса\n"
        "✅ Складской учёт\n"
        "✅ Любой функционал\n\n"
        "⏳ Срок разработки\n"
        "Индивидуально\n"
        "━━━━━━━━━━━━━━━"
    ),
    "tariff_name": "Индивидуальная разработка"
}
}


@dp.callback_query(F.data.in_(TARIF_DETAILS.keys()))
async def show_tarif(callback: CallbackQuery):
    tarif_key = callback.data
    tarif = TARIF_DETAILS[tarif_key]
    photo = FSInputFile(tarif["photo"])

    order_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Заказать", callback_data=f"order_{tarif_key}")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="catalog")]
        ]
    )

    await callback.message.answer_photo(
        photo=photo,
        caption=tarif["caption"],
        reply_markup=order_keyboard
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("order_"))
async def order_tariff(callback: CallbackQuery, state: FSMContext):
    tarif_key = callback.data.replace("order_", "")
    
    # Normalize old/short keys to match TARIF_DETAILS keys
    if tarif_key not in TARIF_DETAILS and f"{tarif_key}_bot" in TARIF_DETAILS:
        tarif_key = f"{tarif_key}_bot"
        
    if tarif_key in TARIF_DETAILS:
        tariff_name = TARIF_DETAILS[tarif_key]["tariff_name"]
    else:
        tariff_name = "Не выбран"

    await state.update_data(tariff=tariff_name)
    await state.set_state(RequestForm.name)

    await callback.message.answer(
        "👤 Введите ваше имя:"
    )
    await callback.answer()
@dp.callback_query(F.data == "order_card")
async def order_card(callback: CallbackQuery, state: FSMContext):

    await state.update_data(
        tariff="Бот-визитка"
    )

    await state.set_state(RequestForm.name)

    await callback.message.answer(
        "👤 Введите ваше имя:"
    )

    await callback.answer()


@dp.callback_query(F.data == "order_shop")
async def order_shop(callback: CallbackQuery, state: FSMContext):

    await state.update_data(
        tariff="Магазин-бот"
    )

    await state.set_state(RequestForm.name)

    await callback.message.answer(
        "👤 Введите ваше имя:"
    )

    await callback.answer()


@dp.callback_query(F.data == "order_ai")
async def order_ai(callback: CallbackQuery, state: FSMContext):

    await state.update_data(
        tariff="AI / ChatGPT бот"
    )

    await state.set_state(RequestForm.name)

    await callback.message.answer(
        "👤 Введите ваше имя:"
    )

    await callback.answer()


@dp.callback_query(F.data == "order_custom")
async def order_custom(callback: CallbackQuery, state: FSMContext):

    await state.update_data(
        tariff="Индивидуальная разработка"
    )

    await state.set_state(RequestForm.name)

    await callback.message.answer(
        "👤 Введите ваше имя:"
    )

    await callback.answer()
@dp.callback_query(F.data == "portfolio")
async def portfolio(callback: CallbackQuery):

    photo = FSInputFile("portfolio.png")

    await callback.message.answer_photo(
        photo=photo,
        caption=
        "🖼 Пример работы\n\n"
       
    )

    await callback.answer()


@dp.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery):

    contact_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Написать менеджеру",
                    url="https://t.me/cg_aza"
                )
            ]
        ]
    )

    await callback.message.answer(
        "📞 Связь с менеджером:",
        reply_markup=contact_keyboard
    )

    await callback.answer()
   
@dp.callback_query(F.data == "request")
async def request_start(callback: CallbackQuery, state: FSMContext):

    await state.set_state(RequestForm.name)

    await callback.message.answer(
        "👤 Введите ваше имя:"
    )

    await callback.answer()


@dp.message(RequestForm.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await state.set_state(RequestForm.phone)

    await message.answer(
        "📱 Введите ваш номер телефона вручную:",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(RequestForm.phone)
async def get_phone(message: Message, state: FSMContext):

    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text

    await state.update_data(phone=phone)

    await state.set_state(RequestForm.comment)

    await message.answer(
        "🛠 Опишите что вас интересует:"
    )


@dp.message(RequestForm.comment)
async def get_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)

    data = await state.get_data()

    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

    text = (
    f"📥 Новая заявка\n\n"
    f"🕒 Дата: {current_time}\n"
    f"👤 Имя: {data['name']}\n"
    f"📱 Телефон: {data['phone']}\n"
    f"💼 Тариф: {data.get('tariff', 'Не выбран')}\n"
    f"📝 Комментарий: {data['comment']}"
)

    await bot.send_message(ADMIN_ID, text)

    sheet.append_row([
    current_time,
    data['name'],
    data['phone'],
    data.get('tariff', 'Не выбран'),
    data['comment']
])

    await message.answer(
    "✅ Заявка отправлена!\n\n"
    "Мы скоро свяжемся с вами.",
    reply_markup=keyboard
)

    await state.clear()

@dp.message(Command("leads"))
async def leads(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    records = sheet.get_all_values()

    if len(records) <= 1:
        await message.answer("Заявок пока нет.")
        return

    text = "📋 Последние заявки\n\n"

    last_records = records[-10:]

    for row in reversed(last_records):

        if len(row) < 5:
            continue

        text += (
            f"🕒 {row[0]}\n"
            f"👤 {row[1]}\n"
            f"📱 {row[2]}\n"
            f"💼 {row[3]}\n\n"
            f"─────────────────\n\n"
        )

    await message.answer(text)
@dp.callback_query(F.data == "ai_consultant")
async def ai_consultant(callback: CallbackQuery, state: FSMContext):

    await state.set_state(AIChat.chat)

    await callback.message.answer(
        "🤖 AI Консультант\n\n"
        "Здравствуйте!\n\n"
        "Я помогу подобрать Telegram-бота для вашего бизнеса.\n\n"
        "Опишите задачу."
    )

    await callback.answer()

@dp.message(AIChat.chat)
async def ai_chat(message: Message):

    user_id = message.from_user.id

    if user_id not in user_history:
        user_history[user_id] = []

    try:

        user_history[user_id].append({
            "role": "user",
            "content": message.text
        })

        messages = [
            {
                "role": "system",
                "content": """
Ты менеджер CG Smart Bots.

Отвечай кратко и по делу.

Не более 5-8 предложений за ответ.

Твоя цель:
- выявить потребность клиента;
- предложить подходящее решение;
- задать следующий вопрос;
- подвести клиента к заявке.

Не пиши длинные статьи.

Когда клиент заинтересован, предложи оставить заявку.

Всегда отвечай на русском языке.
"""
            }
        ]

        messages.extend(user_history[user_id][-10:])

        response = await client_ai.chat.completions.create(
            model="gpt-5.5",
            messages=messages,
            max_completion_tokens=500
        )

        answer_text = response.choices[0].message.content

        user_history[user_id].append({
            "role": "assistant",
            "content": answer_text
        })

        await message.answer(answer_text)

    except Exception as e:

        await message.answer(
            f"Ошибка AI: {e}"
        )

async def main():
    # Запуск веб-сервера для Render (health check)
    from aiohttp import web
    async def handle_health(request):
        return web.Response(text="OK")
    
    port = int(os.getenv("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())