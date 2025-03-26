from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from handlers.reply_handlers import data
from keyboards.inline_keyboards import get_inline_keyboard

router = Router()

# @router.callback_query(lambda c:  c.data.startswith("test_btn_"))
# async def test_callback_handler(callback_query: types.CallbackQuery):
#     data = callback_query.data
#     if data == "test_btn_1":
#         await callback_query.message.edit_text("Edited")
#         await callback_query.answer("You pressed first inline button")
#     elif data == "test_btn_2":
#         await callback_query.message.delete()
#         await callback_query.message.answer("You pressed second inline button", reply_markup=get_inline_test2())

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


def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сортувати за зростанням", callback_data="btn_asc")],
        [InlineKeyboardButton(text="Сортувати за спаданням", callback_data="btn_desc")],
        [InlineKeyboardButton(text="Назад", callback_data="btn_back")]
    ])
    return keyboard

def get_book_button(offer_title):
    return InlineKeyboardButton(text="Забронювати", callback_data=f"book_{offer_title}")

@router.callback_query(lambda c: c.data in ["btn_asc", "btn_desc", "btn_back"])
async def sort_callback(callback_query: types.CallbackQuery):
    sort_order = callback_query.data
    if sort_order == "btn_back":
        # Handle "Back" button - return to the previous state or message.
        await callback_query.message.answer("Ви повернулися до попереднього меню.")
        await show_main_menu(callback_query.message)
    else:
        all_offers = []
        for city in data["cities"]:
            for offer in city["offers"]:
                all_offers.append((city["name"], offer["title"], offer["price"], offer["description"]))

        if sort_order == "btn_asc":
            all_offers.sort(key=lambda x: x[2])  # Сортування за зростанням
        else:
            all_offers.sort(key=lambda x: x[2], reverse=True)  # Сортування за спаданням

        for city_name, title, price, description in all_offers:
            response_text = f"📍 {city_name}: {title}\nЦіна: {price} грн\n{description}"
            await callback_query.message.answer(response_text)

        await callback_query.message.answer("Виберіть опцію сортування:", reply_markup=get_inline_keyboard())


@router.callback_query(lambda c:  c.data.startswith("btn_2."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_2.1":
        await callback_query.message.answer("Ціна(за зростанням):")
    elif data == "btn_2.2":
        await callback_query.message.answer("Ціна(за спаданням):")
    elif data == "btn_2.3":
        await callback_query.message.answer("Введіть назву міста:")
    elif data == "btn_2.4":
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
        await callback_query.message.answer("Ви успішно забронювали тур.")

    # If "btn_4.2" is selected, return to the main menu
    if dis_data == "btn_4.2":
        await callback_query.message.answer("Повернення в головне меню...")
        await show_main_menu(callback_query.message)

@router.callback_query(lambda c:  c.data.startswith("btn_5."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_5.1":
        await callback_query.message.answer("ВИКОНАВ РОБОТУ УЧЕНЬ ГРУПИ П41 БУДНИЙ МАТВІЙ.")
    elif data == "btn_5.2":
        await callback_query.message.answer("Повернення в головне меню...")
        await show_main_menu(callback_query.message)

