import json

from aiogram import types, Router
from aiogram.types import FSInputFile, InlineKeyboardButton

from keyboards.inline_keyboards import get_inline_keyboard, get_inline_keyboard2, get_inline_keyboard3, get_inline_keyboard4, get_inline_keyboard5

router = Router()

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def get_book_button(offer_title):
    return InlineKeyboardButton(text="Забронювати", callback_data=f"book_{offer_title}")


@router.message(lambda message: message.text.startswith("Готові пропозиції"))
async def test_handler(message: types.Message):
    all_offers = []
    for city in data["cities"]:
        for offer in city["offers"]:
            all_offers.append((city["name"], offer["title"], offer["price"], offer["description"]))

    for city_name, title, price, description in all_offers:
        response_text = f"📍 {city_name}: {title}\nЦіна: {price} грн\n{description}"
        await message.answer(response_text)

    await message.answer("Виберіть опцію сортування:", reply_markup=get_inline_keyboard())

    # Check if city name is provided


@router.message(lambda message: message.text == "Пропозиції по містам")
async def test_handler(message: types.Message):
    await message.answer("""Введіть місто щоб знайти події в ньому:""", reply_markup=get_inline_keyboard2())


@router.message(lambda message: message.text == "Бронювання")
async def test_handler(message: types.Message):
    await message.answer("""Тут можна забронювати щось наперед. Напишіть те що ви забронювали:""", reply_markup=get_inline_keyboard3())


@router.message(lambda message: message.text == "Акції")
async def test_handler(message: types.Message):
    offers_with_discount = []

    # Перевірка, що data є списком
    if isinstance(data, dict) and "cities" in data:  # We need to check for the correct structure
        for city in data["cities"]:
            if isinstance(city, dict) and "offers" in city:  # Перевірка наявності ключа "offers"
                for offer in city["offers"]:
                    if isinstance(offer, dict) and "discount" in offer:  # Перевірка наявності знижки
                        offers_with_discount.append(offer)

    # Якщо є пропозиції зі знижкою
    if offers_with_discount:
        for offer in offers_with_discount:
            response_text = f"Тур: {offer['title']}\nЦіна: {offer['price']} грн\nЗнижка: {offer['discount']}\nОпис: {offer['description']}\n"
            await message.answer(response_text, reply_markup=get_inline_keyboard4())  # Send each offer as a separate message
    else:
        await message.answer("На даний момент немає доступних акцій.", reply_markup=get_inline_keyboard4())


@router.message(lambda message: message.text == "Контакти")
async def test_handler(message: types.Message):
    await message.answer("""Тут є контакти розробника.Нажми на кнопку щоб дізнатися їх.""",
                         reply_markup=get_inline_keyboard5())


@router.message(lambda message: message.text == "Пасхалочка")
async def test_handler(message: types.Message):
    photo = FSInputFile(r"C:\Users\asus\Documents\GitHub\TravelBot\assets\playboi-carti-gq-december-january-2021-02.jpg")  # Замініть шлях на реальний шлях до зображення
    await message.answer_photo(photo, caption="Ось ваша пасхалочка! 🐣")
