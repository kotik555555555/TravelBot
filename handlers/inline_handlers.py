from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from handlers.reply_handlers import data
from keyboards.inline_keyboards import get_inline_keyboard1, get_sorting_keyboard

router = Router()


async def show_main_menu(message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Готові пропозиції"), KeyboardButton(text="Пропозиції по містам")],
            [KeyboardButton(text="Бронювання"), KeyboardButton(text="Акції")],
            [KeyboardButton(text="Контакти"), KeyboardButton(text="Пасхалочка")]
        ],
        resize_keyboard=True
    )
    await message.answer("Головне меню:", reply_markup=keyboard)

# Callback handler for price sorting buttons
def find_city(city_name):
    city_name = city_name.strip().lower()
    for city in data.get("cities", []):
        if city["name"].strip().lower() == city_name:
            print(f"✅ Місто знайдено: {city['name']}")
            return city
    print("⚠ Місто не знайдено у списку!")
    return None



@router.callback_query(lambda c: c.data in ["btn_asc", "btn_desc", "btn_back"])
async def sort_callback(callback_query: types.CallbackQuery):
    sort_order = callback_query.data

    if sort_order == "btn_back":
        # Повернення до головного меню
        await callback_query.message.answer("🔙 Ви повернулися до попереднього меню.")
        await show_main_menu(callback_query.message)
        return

    # Отримуємо всі пропозиції
    all_offers = [
        (city.get("name"), offer.get("title"), offer.get("price"), offer.get("description"), offer.get("image"))
        for city in data.get("cities", []) if isinstance(city, dict)
        for offer in city.get("offers", []) if isinstance(offer, dict)
    ]

    # Сортування за ціною (перетворюємо на число)
    reverse_order = sort_order == "btn_desc"
    all_offers.sort(key=lambda x: float(x[2]) if str(x[2]).replace('.', '', 1).isdigit() else 0, reverse=reverse_order)

    # Відправляємо відсортовані пропозиції
    for city_name, title, price, description, image in all_offers:
        response_text = (
            f"📍 *{city_name}: {title}*\n"
            f"💰 *Ціна:* {price} грн\n"
            f"📖 {description}"
        )
        if image:
            await callback_query.message.answer_photo(photo=image, caption=response_text, parse_mode="Markdown")
        else:
            await callback_query.message.answer(response_text, parse_mode="Markdown")

    # Пропонуємо вибір сортування знову
    await callback_query.message.answer("📊 Виберіть опцію сортування:", reply_markup=get_inline_keyboard1())



@router.callback_query(lambda c:  c.data.startswith("btn_2."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_2.1":
        await callback_query.message.answer("Введіть назву міста:")
    elif data == "btn_2.2":
        await callback_query.message.answer("Повернення в головне меню...")
        await show_main_menu(callback_query.message)

@router.callback_query(lambda c:  c.data.startswith("btn_3."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_3.1":
        await callback_query.message.answer("Опишіть ваше замовлення:")
    elif data == "btn_3.2":
        await callback_query.message.answer("Повернення в головне меню...")
        await show_main_menu(callback_query.message)


@router.callback_query(lambda c: c.data.startswith("btn_4."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    dis_data = callback_query.data  # Callback data (e.g., "btn_4.1")

    if dis_data == "btn_4.1":
        # Фільтруємо тільки тури зі знижкою
        offers = [
            offer
            for city in data.get("cities", [])
            if isinstance(city, dict)
            for offer in city.get("offers", [])
            if isinstance(offer, dict) and "discount" in offer
        ]
    elif dis_data == "btn_4.2":
        # Всі тури без фільтрації
        offers = [
            offer
            for city in data.get("cities", [])
            if isinstance(city, dict)
            for offer in city.get("offers", [])
            if isinstance(offer, dict)
        ]
    else:
        return

    if offers:
        # Вибір способу сортування
        await callback_query.message.answer("🔽 Виберіть спосіб сортування:", reply_markup=get_sorting_keyboard())
    else:
        await callback_query.message.answer("🔸 Наразі немає доступних акцій.")
        return


@router.callback_query(lambda c: c.data.startswith("sort_"))
async def sort_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "sort_back":
        # Повернення до головного меню при натисканні кнопки "Назад"
        await callback_query.message.answer("🔙 Ви повернулися до попереднього меню.")
        await show_main_menu(callback_query.message)
        return

    sort_order = callback_query.data.split("_")[1]  # sort_asc або sort_desc

    # Фільтруємо пропозиції тільки з знижками
    offers_with_discount = [
        offer
        for city in data.get("cities", [])
        if isinstance(city, dict)
        for offer in city.get("offers", [])
        if isinstance(offer, dict) and "discount" in offer
    ]

    if not offers_with_discount:
        await callback_query.message.answer("🔸 Наразі немає доступних акцій.")
        return

    # Сортування пропозицій за ціною
    reverse_order = sort_order == "desc"
    offers_with_discount.sort(key=lambda x: float(x["price"]) if str(x["price"]).replace('.', '', 1).isdigit() else 0, reverse=reverse_order)

    # Відправляємо відсортовані пропозиції
    for offer in offers_with_discount:
        city_name = offer.get("city", "Невідоме місто")
        title = offer.get("title", "Без назви")
        price = offer.get("price", "Не вказана ціна")
        description = offer.get("description", "Без опису")
        image = offer.get("image", None)

        response_text = (
            f"📍 *{city_name}: {title}*\n"
            f"💰 *Ціна:* {price} грн\n"
            f"🎉 *Знижка:* {offer.get('discount', 'Не вказано')}%\n"
            f"📖 {description}"
        )

        if image:
            await callback_query.message.answer_photo(photo=image, caption=response_text, parse_mode="Markdown", reply_markup=get_sorting_keyboard())
        else:
            await callback_query.message.answer(response_text, parse_mode="Markdown", reply_markup=get_sorting_keyboard())



@router.callback_query(lambda c:  c.data.startswith("btn_5."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_5.1":
        await callback_query.message.answer("📚 ВИКОНАВ РОБОТУ УЧЕНЬ ГРУПИ П41 БУДНИЙ МАТВІЙ. 🎓")
    elif data == "btn_5.2":
        await callback_query.message.answer("🔙 Повернення в головне меню... 🏠")
        await show_main_menu(callback_query.message)
