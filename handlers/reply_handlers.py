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
    all_offers = [
        (city.get("name"), offer.get("title"), offer.get("price"), offer.get("description"), offer.get("image"))
        for city in data.get("cities", []) if isinstance(city, dict)
        for offer in city.get("offers", []) if isinstance(offer, dict)
    ]

    if all_offers:
        for city_name, title, price, description, image in all_offers:
            response_text = (
                f"📍 *{city_name}: {title}*\n"
                f"💰 *Ціна:* {price} грн\n"
                f"📖 {description}"
            )
            if image:  # Якщо є фото, надсилаємо його
                await message.answer_photo(photo=image, caption=response_text, parse_mode="Markdown")
            else:  # Якщо фото немає, відправляємо просто текст
                await message.answer(response_text, parse_mode="Markdown")

        await message.answer("📊 Виберіть опцію сортування:", reply_markup=get_inline_keyboard())
    else:
        await message.answer("❌ Наразі немає доступних пропозицій.", reply_markup=get_inline_keyboard())


@router.message(lambda message: message.text == "Пропозиції по містам")
async def test_handler(message: types.Message):
    await message.answer("""Введіть місто щоб знайти події в ньому:""", reply_markup=get_inline_keyboard2())


@router.message(lambda message: message.text == "Бронювання")
async def test_handler(message: types.Message):
    await message.answer("""Тут можна забронювати щось наперед. Напишіть те що ви забронювали:""", reply_markup=get_inline_keyboard3())


@router.message(lambda message: message.text == "Акції")
async def test_handler(message: types.Message):
    # Отримуємо всі пропозиції зі знижкою
    offers_with_discount = [
        offer
        for city in data.get("cities", [])
        if isinstance(city, dict)
        for offer in city.get("offers", [])
        if isinstance(offer, dict) and "discount" in offer
    ]

    if offers_with_discount:
        for offer in offers_with_discount:
            response_text = (
                f"🏝 *{offer['title']}*\n"
                f"💰 *Ціна:* {offer['price']} грн\n"
                f"🎉 *Знижка:* {offer['discount']}%\n"
                f"📖 *Опис:* {offer['description']}"
            )
            if "image" in offer and offer["image"]:  # Якщо є картинка
                await message.answer_photo(photo=offer["image"], caption=response_text, reply_markup=get_inline_keyboard4(), parse_mode="Markdown")
            else:
                await message.answer(response_text, reply_markup=get_inline_keyboard4(), parse_mode="Markdown")
    else:
        await message.answer("🔸 Наразі немає доступних акцій.", reply_markup=get_inline_keyboard4())


@router.message(lambda message: message.text == "Контакти")
async def test_handler(message: types.Message):
    await message.answer("""Тут є контакти розробника.Нажми на кнопку щоб дізнатися їх.""",
                         reply_markup=get_inline_keyboard5())


@router.message(lambda message: message.text == "Пасхалочка")
async def test_handler(message: types.Message):
    # Use baselib FileManager to manage the image path
    photo = FSInputFile("assets/playboi-carti-gq-december-january-2021-02.jpg")  # Pass the resolved file path to FSInputFile
    await message.answer_photo(photo, caption="Ось ваша пасхалочка! 🐣")
