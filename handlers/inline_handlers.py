import json

import aiofiles
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from handlers.reply_handlers import data
from keyboards.inline_keyboards import get_inline_keyboard1, get_sorting_keyboard
from keyboards.reply_keyboards import show_main_menu
from aiogram.fsm.state import State, StatesGroup

router = Router()
bookings = {}

class BookingState(StatesGroup):
    waiting_for_city = State()     # Очікуємо введення міста
    waiting_for_offer = State()

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


async def load_city_data():
    try:
        async with aiofiles.open("data.json", "r", encoding="utf-8") as file:
            content = await file.read()
        print("DEBUG: Successfully loaded city data.")  # Debug log
        return json.loads(content)
    except FileNotFoundError:
        raise FileNotFoundError("Файл з даними не знайдено. Перевірте файл.")
    except json.JSONDecodeError:
        raise ValueError("Помилка у форматі файлу JSON. Перевірте його.")
    except Exception as e:
        raise Exception(f"Помилка при зчитуванні файлу: {str(e)}")

# Handler for city input
@router.message(BookingState.waiting_for_city, F.text)
async def handle_city_name(message: types.Message, state: FSMContext):
    city_name = message.text.strip()

    if not city_name:
        await message.answer("⚠ Ви не ввели назву міста. Спробуйте ще раз.")
        return

    print(f"DEBUG: Введена назва міста: {city_name}")

    try:
        city_data = await load_city_data()
        cities = city_data.get("cities", [])

        if not isinstance(cities, list):
            raise ValueError("Очікувався список міст у ключі 'cities'")

        # Search for the city
        city = next((c for c in cities if c.get("name").lower() == city_name.lower()), None)

        if city:
            response = (
                f"🏙 Місто: {city['name']}\n"
                f"🇺🇦 Країна: {city['country']}\n\n"
                f"💰 Пропозиції:\n"
            )
            await message.answer(response)

            # Send offers
            for offer in city.get("offers", []):
                offer_response = f"- {offer['title']} ({offer['price']} грн)\n  {offer['description']}\n"
                if "image" in offer:
                    await message.answer_photo(offer['image'], caption=offer_response)
                else:
                    await message.answer(offer_response)

    except (FileNotFoundError, json.JSONDecodeError, ValueError, Exception) as e:
        await message.answer(f"⚠ Помилка: {str(e)}")
        print(f"[ERROR] {e}")

# Handler for the city selection callback
@router.callback_query(lambda c: c.data == "btn_2.1")
async def city_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    print(f"DEBUG: callback_query.data = {callback_query.data}")  # Debug log
    await state.set_state(BookingState.waiting_for_city)  # Set the state to wait for city name input
    await callback_query.message.answer("Введіть назву міста:")

# Handler for the back button callback
@router.callback_query(lambda c: c.data == "btn_2.2")
async def back_to_main_menu(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Повернення в головне меню...")
    await show_main_menu(callback_query.message)

# Handler for offer selection input
@router.message(BookingState.waiting_for_offer)
async def handle_offer_name(message: types.Message, state: FSMContext):
    offer_name = message.text.strip().lower()
    print(f"DEBUG: Введена назва пропозиції: {offer_name}")

    try:
        # Завантажуємо дані про міста та пропозиції
        city_data = await load_city_data()
        found_offer, found_city = None, None

        # Пошук пропозиції по назві
        for city in city_data.get("cities", []):
            for offer in city.get("offers", []):
                if offer["title"].lower() == offer_name:
                    found_offer, found_city = offer, city["name"]
                    break
            if found_offer:
                break

        if found_offer:
            # Отримуємо URL зображення з JSON
            image_url = found_offer.get("image", None)

            # Відправка повідомлення з зображенням або без
            await send_offer_message(message, found_offer, found_city, image_url)

            # Оновлюємо стан користувача
            await state.update_data(selected_city=found_city, selected_offer=found_offer["title"])

        else:
            await message.answer("⚠ Пропозицію не знайдено. Спробуйте ще раз.")

    except Exception as e:
        print(f"[ERROR] {e}")
        await message.answer("⚠ Виникла помилка. Спробуйте пізніше.")


async def send_offer_message(message, offer, city, image_url):
    """
    Функція для відправлення повідомлення з пропозицією, може включати зображення.
    """
    offer_details = (
        f"✅ Ви забронювали пропозицію: {offer['title']}\n\n"
        f"📍 Місто: {city}\n🎭 Назва: {offer['title']}\n"
        f"💰 Ціна: {offer['price']} грн\n📜 Опис: {offer['description']}"
    )

    if image_url:
        await message.answer_photo(
            photo=image_url,
            caption=offer_details
        )
    else:
        await message.answer(offer_details)

@router.callback_query(lambda c: c.data.startswith("btn_3."))
async def city_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == "btn_3.1":
        await callback_query.message.answer("📝 Опишіть ваше замовлення: (Наприклад, виберіть пропозицію за назвою)")
        await state.set_state(BookingState.waiting_for_offer)
    elif data == "btn_3.2":
        await callback_query.message.answer("🔙 Повернення в головне меню...")
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
