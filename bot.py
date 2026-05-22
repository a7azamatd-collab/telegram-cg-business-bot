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
    "credentials.json",
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
                text="📋 Услуги",
                callback_data="services"
            )
        ],
        [
            InlineKeyboardButton(
                text="💰 Цены",
                callback_data="prices"
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
@dp.callback_query(F.data == "services")
async def services(callback: CallbackQuery):
    await callback.message.answer(
        "🔹 Создание Telegram-ботов\n"
        "🔹 Боты для бизнеса\n"
        "🔹 Автоматизация заявок"
    )

    await callback.answer()


@dp.callback_query(F.data == "prices")
async def prices(callback: CallbackQuery):
    await callback.message.answer(
        "💰 Цены на услуги\n\n"

        "🔹 Базовый бот — от 20 000 ₸\n"
        "• Меню с кнопками\n"
        "• Сбор заявок\n"
        "• Контакты и FAQ\n\n"

        "🔹 Бизнес бот — от 50 000 ₸\n"
        "• Каталог товаров\n"
        "• Запись клиентов\n"
        "• Фото и карточки товаров\n"
        "• Уведомления администратору\n\n"

        "🔹 Продвинутый бот — от 100 000 ₸\n"
        "• AI / ChatGPT функции\n"
        "• CRM интеграции\n"
        "• Автоматизация бизнеса\n"
        "• Индивидуальный функционал"
    )
    
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