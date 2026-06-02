import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = "8813038337:AAFJFQmFxyjBX_W_gaetx-WVr7xRk6SnHv0"

ADMIN_ID = 490936540

bot = Bot(token=TOKEN)
dp = Dispatcher()

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "/etc/secrets/credentials.json",
    scope
)

client = gspread.authorize(creds)

sheet = client.open("CRM Заявки").sheet1

class RequestForm(StatesGroup):
    name = State()
    phone = State()
    comment = State()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
   
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
        "💼 Каталог решений\n\n"
        "Выберите интересующий вариант:",
        reply_markup=catalog_keyboard
    )

    await callback.answer()
@dp.callback_query(F.data == "business_bot")
async def business_bot(callback: CallbackQuery):

    photo = FSInputFile("tarif/business.png")

    order_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Заказать", callback_data="order_business")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="catalog")]
        ]
    )

    await callback.message.answer_photo(
    photo=photo,
    caption=
        "━━━━━━━━━━━━━━━\n"
        "🔹 БИЗНЕС-БОТ\n\n"

        "💰 Стоимость\n"
        "от 70 000 ₸\n\n"

        "🔄 Поддержка\n"
        "50 000 ₸ / месяц\n\n"

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
        "3–7 дней\n"
        "━━━━━━━━━━━━━━━",

        reply_markup=order_keyboard
    )

    await callback.answer()
@dp.callback_query(F.data == "card_bot")
async def card_bot(callback: CallbackQuery):

    photo = FSInputFile("tarif/visitka.png")

    order_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Заказать", callback_data="order_card")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="catalog")]
        ]
    )

    await callback.message.answer_photo(
    photo=photo,
    caption=
        "━━━━━━━━━━━━━━━\n"
        "🔹 БОТ-ВИЗИТКА\n\n"

        "💰 Стоимость\n"
        "от 50 000 ₸\n\n"

        "🔄 Поддержка\n"
        "30 000 ₸ / месяц\n\n"

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
        "1–3 дня\n"
        "━━━━━━━━━━━━━━━",

        reply_markup=order_keyboard
    )

    await callback.answer()
@dp.callback_query(F.data == "shop_bot")
async def shop_bot(callback: CallbackQuery):

    photo = FSInputFile("tarif/shop.png")

    order_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Заказать", callback_data="order_shop")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="catalog")]
        ]
    )

    await callback.message.answer_photo(
    photo=photo,
    caption=
        "━━━━━━━━━━━━━━━\n"
        "🛍 МАГАЗИН-БОТ\n\n"

        "💰 Стоимость\n"
        "от 120 000 ₸\n\n"

        "🔄 Поддержка\n"
        "70 000 ₸ / месяц\n\n"

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
        "7–14 дней\n"
        "━━━━━━━━━━━━━━━",

        reply_markup=order_keyboard
    )

    await callback.answer()
@dp.callback_query(F.data == "ai_bot")
async def ai_bot(callback: CallbackQuery):

    photo = FSInputFile("tarif/ai.png")

    order_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Заказать", callback_data="order_ai")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="catalog")]
        ]
    )

    await callback.message.answer_photo(
    photo=photo,
    caption=
        "━━━━━━━━━━━━━━━\n"
        "🤖 AI / CHATGPT БОТ\n\n"

        "💰 Стоимость\n"
        "от 150 000 ₸\n\n"

        "🔄 Поддержка\n"
        "100 000 ₸ / месяц\n\n"

        "📦 Что входит\n\n"

        "✅ AI-консультант\n"
        "✅ ChatGPT интеграция\n"
        "✅ Ответы клиентам 24/7\n"
        "✅ Автоматизация продаж\n"
        "✅ CRM интеграции\n"
        "✅ Индивидуальное обучение\n\n"

        "⏳ Срок разработки\n"
        "7–14 дней\n"
        "━━━━━━━━━━━━━━━",

        reply_markup=order_keyboard
    )

    await callback.answer()
@dp.callback_query(F.data == "custom_bot")
async def custom_bot(callback: CallbackQuery):

    photo = FSInputFile("tarif/custom.png")

    order_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Заказать", callback_data="order_custom")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="catalog")]
        ]
    )

    await callback.message.answer_photo(
    photo=photo,
    caption=
        "━━━━━━━━━━━━━━━\n"
        "⚙ ИНДИВИДУАЛЬНАЯ РАЗРАБОТКА\n\n"

        "💰 Стоимость\n"
        "от 200 000 ₸\n\n"

        "📦 Возможности\n\n"

        "✅ Telegram Mini App\n"
        "✅ Онлайн-оплата\n"
        "✅ CRM интеграции\n"
        "✅ Автоматизация бизнеса\n"
        "✅ Складской учёт\n"
        "✅ Любой функционал\n\n"

        "⏳ Срок разработки\n"
        "Индивидуально\n"
        "━━━━━━━━━━━━━━━",

        reply_markup=order_keyboard
    )

    await callback.answer()
@dp.callback_query(F.data == "order_business")
async def order_business(callback: CallbackQuery, state: FSMContext):

    await state.update_data(
        tariff="Бизнес-бот"
    )

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

    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Отправить номер",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
    "📱 Отправьте номер кнопкой ниже.\n\n"
    "Если вы используете Telegram на ПК, просто введите номер вручную.",
    reply_markup=contact_keyboard
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

@dp.message(F.text == "/stat")
async def stat(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    records = sheet.get_all_values()

    total = len(records) - 1

    visitka = 0
    business = 0
    shop = 0
    ai = 0
    custom = 0

    for row in records[1:]:

        if len(row) < 4:
            continue

        tariff = row[3]

        if tariff == "Бот-визитка":
            visitka += 1

        elif tariff == "Бизнес-бот":
            business += 1

        elif tariff == "Магазин-бот":
            shop += 1

        elif tariff == "AI / ChatGPT бот":
            ai += 1

        elif tariff == "Индивидуальная разработка":
            custom += 1

    await message.answer(
        f"📊 Статистика заявок\n\n"
        f"Всего заявок: {total}\n\n"
        f"🔹 Бот-визитка: {visitka}\n"
        f"🔹 Бизнес-бот: {business}\n"
        f"🛍 Магазин-бот: {shop}\n"
        f"🤖 AI / ChatGPT бот: {ai}\n"
        f"⚙ Индивидуальная разработка: {custom}"
    )

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())