# Імпортуємо потрібні модулі
import json
import aiofiles
import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from urllib.parse import urlparse
import html

# Імпорт внутрішніх модулів
from handlers.reply_handlers import data
from keyboards.inline_keyboards import get_inline_keyboard, get_sorting_keyboard
from keyboards.reply_keyboards import show_main_menu
from aiogram.fsm.state import State, StatesGroup

# Ініціалізація маршрутизатора
router = Router()
bookings = {}  # Словник для збереження бронювань

# Визначаємо стани FSM
class BookingState(StatesGroup):
    waiting_for_city = State()     # Очікуємо введення міста
    waiting_for_offer = State()    # Очікуємо введення назви пропозиції

# Допоміжна функція для пошуку міста за назвою
def find_city(city_name):
    city_name = city_name.strip().lower()
    for city in data.get("cities", []):
        if city["name"].strip().lower() == city_name:
            print(f"✅ Місто знайдено: {city['name']}")
            return city
    print("⚠ Місто не знайдено у списку!")
    return None

# Обробник callback'ів для сортування за ціною
@router.callback_query(lambda c: c.data in ["btn_asc", "btn_desc", "btn_back"])
async def sort_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "btn_back":
        await show_main_menu(callback_query.message)
        return

    sort_order = callback_query.data.split("_")[1]  # 'asc' або 'desc'

    # Збираємо всі пропозиції з усіх міст
    all_offers = []
    for city in data.get("cities", []):
        if isinstance(city, dict):
            city_name = city.get("name", "Невідоме місто")
            for offer in city.get("offers", []):
                if isinstance(offer, dict):
                    offer["city"] = city_name
                    all_offers.append(offer)

    if not all_offers:
        await callback_query.message.answer("🔸 Наразі немає доступних пропозицій.", reply_markup=get_inline_keyboard())
        return

    # Сортування за ціною
    reverse_order = sort_order == "desc"
    all_offers.sort(
        key=lambda x: float(x["price"]) if str(x["price"]).replace('.', '', 1).isdigit() else 0,
        reverse=reverse_order
    )

    # Допоміжна функція для перевірки URL
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme in ('http', 'https'), result.netloc])
        except:
            return False

    # Формуємо повідомлення для надсилання
    messages = []
    current_block = ""

    for offer in all_offers:
        city_name = html.escape(offer.get("city", "Невідоме місто"))
        title = html.escape(offer.get("title", "Без назви"))
        price = html.escape(str(offer.get("price", "Не вказано")))
        description = html.escape(offer.get("description", "Без опису"))
        image = offer.get("image")

        offer_text = (
            f"<b>📍 {city_name}: {title}</b>\n"
            f"<b>💰 Ціна:</b> {price} грн\n"
            f"<b>📖 Опис:</b> {description}\n"
        )

        if image and is_valid_url(image):
            offer_text += f"<a href=\"{html.escape(image, quote=True)}\">🖼️ Фото пропозиції</a>\n"

        offer_text += "\n\n"

        if len(current_block) + len(offer_text) <= 4096:
            current_block += offer_text
        else:
            messages.append(current_block.strip())
            current_block = offer_text

    if current_block:
        messages.append(current_block.strip())

    # Надсилаємо сформовані блоки повідомлень
    for msg in messages:
        try:
            await callback_query.message.answer(msg, parse_mode="HTML", disable_web_page_preview=False)
        except aiogram.exceptions.TelegramBadRequest as e:
            await callback_query.message.answer(
                f"⚠️ Помилка:\n<code>{html.escape(str(e))}</code>",
                parse_mode="HTML"
            )

    await callback_query.message.answer("📊 Виберіть спосіб сортування:", reply_markup=get_inline_keyboard())

# Завантаження JSON-даних міст
async def load_city_data():
    try:
        async with aiofiles.open("data.json", "r", encoding="utf-8") as file:
            content = await file.read()
        print("DEBUG: Successfully loaded city data.")
        return json.loads(content)
    except FileNotFoundError:
        raise FileNotFoundError("⚠ Файл з даними не знайдено. Перевірте файл.")
    except json.JSONDecodeError:
        raise ValueError("❗ Помилка у форматі файлу JSON. Перевірте його.")
    except Exception as e:
        raise Exception(f"⚠ Помилка при зчитуванні файлу: {str(e)}")

# Обробник введення міста
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
            raise ValueError("❗ Очікувався список міст у ключі 'cities'")

        city = next((c for c in cities if c.get("name").lower() == city_name.lower()), None)

        if city:
            response = (
                f"🏙 <b>Місто:</b> {html.escape(city['name'])}\n"
                f"🇺🇦 <b>Країна:</b> {html.escape(city['country'])}\n\n"
                f"💰 <b>Пропозиції:</b>\n\n"
            )

            offers = city.get("offers", [])
            if offers:
                for offer in offers:
                    title = html.escape(offer.get("title", "Без назви"))
                    price = html.escape(str(offer.get("price", "Невідомо")))
                    description = html.escape(offer.get("description", "Без опису"))
                    image = offer.get("image")

                    offer_text = (
                        f"🔹 <b>{title}</b>\n"
                        f"💵 <b>Ціна:</b> {price} грн\n"
                        f"📖 {description}\n"
                    )

                    if image:
                        offer_text += f'<a href="{html.escape(image, quote=True)}">🖼️ Фото пропозиції</a>\n'

                    response += offer_text + "\n"
            else:
                response += "❌ Наразі немає доступних пропозицій.\n"

            # Надсилаємо у частинах, якщо перевищено ліміт символів
            if len(response) <= 4096:
                await message.answer(response.strip(), parse_mode="HTML", disable_web_page_preview=False)
            else:
                chunks = []
                current = ""
                for block in response.split("\n\n"):
                    if len(current) + len(block) + 2 <= 4096:
                        current += block + "\n\n"
                    else:
                        chunks.append(current.strip())
                        current = block + "\n\n"
                if current:
                    chunks.append(current.strip())

                for part in chunks:
                    await message.answer(part, parse_mode="HTML", disable_web_page_preview=False)

        else:
            await message.answer("⚠ Місто не знайдено. Спробуйте ще раз.")
            return

    except (FileNotFoundError, json.JSONDecodeError, ValueError, Exception) as e:
        await message.answer(f"⚠ Помилка: {str(e)}")
        print(f"[ERROR] {e}")



# Обробник callback-запиту при виборі міста
@router.callback_query(lambda c: c.data == "btn_2.1")
async def city_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    print(f"DEBUG: callback_query.data = {callback_query.data}")  # Виведення debug-інформації
    await state.set_state(BookingState.waiting_for_city)  # Встановлення стану очікування введення міста
    await callback_query.message.answer("📝 Введіть назву міста:")

# Обробник повернення до головного меню
@router.callback_query(lambda c: c.data == "btn_2.2")
async def back_to_main_menu(callback_query: types.CallbackQuery):
    await show_main_menu(callback_query.message)  # Показ головного меню

# Обробник введення назви пропозиції користувачем
@router.message(BookingState.waiting_for_offer)
async def handle_offer_name(message: types.Message, state: FSMContext):
    offer_name = message.text.strip().lower()
    print(f"DEBUG: Введена назва пропозиції: {offer_name}")

    try:
        city_data = await load_city_data()  # Завантаження JSON-даних
        found_offer, found_city = None, None

        # Пошук відповідної пропозиції серед усіх міст
        for city in city_data.get("cities", []):
            for offer in city.get("offers", []):
                if offer["title"].lower() == offer_name:
                    found_offer, found_city = offer, city["name"]
                    break
            if found_offer:
                break

        if found_offer:
            image_url = found_offer.get("image", None)  # URL зображення
            await send_offer_message(message, found_offer, found_city, image_url)  # Надсилання повідомлення
            await state.update_data(selected_city=found_city, selected_offer=found_offer["title"])  # Оновлення стану
        else:
            await message.answer("⚠ Пропозицію не знайдено. Спробуйте ще раз.")

    except Exception as e:
        print(f"[ERROR] {e}")
        await message.answer("⚠ Виникла помилка. Спробуйте пізніше.")

# Функція для надсилання повідомлення про пропозицію
async def send_offer_message(message, offer, city, image_url):
    offer_details = (
        f"✅ <b>Ви забронювали пропозицію</b>: <b>{offer['title']}</b>\n\n"
        f"📍 <b>Місто:</b> {city}\n"
        f"🎭 <b>Назва:</b> {offer['title']}\n"
        f"💰 <b>Ціна:</b> {offer['price']} грн\n"
        f"📜 <b>Опис:</b> {offer['description']}"
    )

    if image_url:
        await message.answer_photo(photo=image_url, caption=offer_details, parse_mode="HTML")
    else:
        await message.answer(offer_details, parse_mode="HTML")


# Обробка кнопок, пов'язаних з вибором пропозиції або поверненням
@router.callback_query(lambda c: c.data.startswith("btn_3."))
async def city_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == "btn_3.1":
        await callback_query.message.answer("📝 Опишіть ваше замовлення: (Наприклад, виберіть пропозицію за назвою)")
        await state.set_state(BookingState.waiting_for_offer)
    elif data == "btn_3.2":
        await show_main_menu(callback_query.message)

# Обробка кнопок з категорії знижок
@router.callback_query(lambda c: c.data.startswith("btn_4."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    dis_data = callback_query.data

    if dis_data == "btn_4.1":
        # Фільтрація лише акційних пропозицій
        offers = [
            offer for city in data.get("cities", [])
            if isinstance(city, dict)
            for offer in city.get("offers", [])
            if isinstance(offer, dict) and "discount" in offer
        ]
    elif dis_data == "btn_4.2":
        # Всі пропозиції
        offers = [
            offer for city in data.get("cities", [])
            if isinstance(city, dict)
            for offer in city.get("offers", [])
            if isinstance(offer, dict)
        ]
    else:
        return

    if offers:
        await callback_query.message.answer("🔽 Виберіть спосіб сортування:", reply_markup=get_sorting_keyboard())
    else:
        await callback_query.message.answer("🔸 Наразі немає доступних акцій.")
        return

# Сортування пропозицій зі знижками
@router.callback_query(lambda c: c.data.startswith("sort_"))
async def sort_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "sort_back":
        await show_main_menu(callback_query.message)
        return

    sort_order = callback_query.data.split("_")[1]
    reverse_order = sort_order == "desc"

    offers_with_discount = [
        offer for city in data.get("cities", [])
        if isinstance(city, dict)
        for offer in city.get("offers", [])
        if isinstance(offer, dict) and "discount" in offer
    ]

    if not offers_with_discount:
        await callback_query.message.answer("🔸 Наразі немає доступних акцій.")
        return

    offers_with_discount.sort(
        key=lambda x: float(x["price"]) if str(x["price"]).replace('.', '', 1).isdigit() else 0,
        reverse=reverse_order
    )

    # Формування тексту всіх пропозицій
    offer_texts = ""
    for offer in offers_with_discount:
        city_name = offer.get("city", "Невідоме місто")
        title = offer.get("title", "Без назви")
        price = offer.get("price", "Не вказана ціна")
        description = offer.get("description", "Без опису")
        discount = offer.get("discount", "Не вказано")
        image = offer.get("image")

        offer_text = (
            f"📍 *{city_name}: {title}*\n"
            f"💰 *Ціна:* {price} грн\n"
            f"🎉 *Знижка:* {discount}%\n"
            f"📖 {description}\n"
        )

        if image:
            offer_text += f"🖼️ [Фото пропозиції]({image})\n"

        offer_texts += offer_text + "\n\n"

    if offer_texts:
        for i in range(0, len(offer_texts), 4096):  # Telegram обмеження на довжину повідомлення
            await callback_query.message.answer(offer_texts[i:i + 4096], parse_mode="Markdown", disable_web_page_preview=False)

        await callback_query.message.answer("📊 Виберіть спосіб сортування:", reply_markup=get_sorting_keyboard())
    else:
        await callback_query.message.answer("🔸 Наразі немає доступних акцій.", reply_markup=get_sorting_keyboard())

# Обробка інформаційних кнопок (хто автор тощо)
@router.callback_query(lambda c: c.data.startswith("btn_5."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_5.1":
        await callback_query.message.answer("📚 ВИКОНАВ РОБОТУ УЧЕНЬ ГРУПИ П41 БУДНИЙ МАТВІЙ. 🎓")
    elif data == "btn_5.2":
        await show_main_menu(callback_query.message)

# Обробка підтвердження користувачем
@router.callback_query(lambda c: c.data == "btn_yes")
async def handle_yes_callback(callback: types.CallbackQuery):
    await callback.answer()  # Знімає індикатор завантаження з кнопки
    await callback.message.answer("🎉 Чудово, що все збігається! НЕ ЗБРЕХАВ!")

# Обробка відмови користувача
@router.callback_query(lambda c: c.data == "btn_no")
async def handle_no_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("👁️ НЕ БРЕШИ... Я БАЧУ ВСЕ. 🕵️‍♂️ Це точно твої дані!")

# Обробка ще однієї категорії кнопок (наприклад, вихід)
@router.callback_query(lambda c: c.data.startswith("btn_6."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_6.3":
        await show_main_menu(callback_query.message)  # Повернення до головного меню
