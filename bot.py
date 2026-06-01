import asyncio
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
    service = State()


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

    order_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Заказать", callback_data="request")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="catalog")]
        ]
    )

    await callback.message.answer(
        "━━━━━━━━━━━━━━━\n"
        "🔹 БИЗНЕС-БОТ\n\n"

        "💰 Стоимость\n"
        "от 50 000 ₸\n\n"

        "🔄 Поддержка\n"
        "10 000 ₸ / месяц\n\n"

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
        "📱 Нажмите кнопку ниже чтобы отправить номер:",
        reply_markup=contact_keyboard
    )


@dp.message(RequestForm.phone)
async def get_phone(message: Message, state: FSMContext):

    phone = message.contact.phone_number

    await state.update_data(phone=phone)

    await state.set_state(RequestForm.service)

    await message.answer(
        "🛠 Опишите что вас интересует:"
    )


@dp.message(RequestForm.service)
async def get_service(message: Message, state: FSMContext):
    await state.update_data(service=message.text)

    data = await state.get_data()

    text = (
        f"📥 Новая заявка\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"🛠 Услуга: {data['service']}"
    )

    await bot.send_message(ADMIN_ID, text)

    sheet.append_row([
    data['name'],
    data['phone'],
    data['service']
])

    await message.answer(
    "✅ Заявка отправлена!\n\n"
    "Мы скоро свяжемся с вами.",
    reply_markup=keyboard
)

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())