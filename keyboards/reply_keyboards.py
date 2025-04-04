from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    # Додаємо емодзі в кнопки
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="""🎉 Готові пропозиції"""), KeyboardButton(text="""🏙️ Пропозиції по містам""")],
            [KeyboardButton(text="""🛏️ Бронювання"""), KeyboardButton(text="""🎈 Акції""")],
            [KeyboardButton(text="""📞 Контакти"""), KeyboardButton(text="""🐣 Пасхалочка""")]
        ],
        resize_keyboard=True
    )
    return keyboard

async def show_main_menu(message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎉 Готові пропозиції"), KeyboardButton(text="🏙️ Пропозиції по містам")],
            [KeyboardButton(text="🛏️ Бронювання"), KeyboardButton(text="🎈 Акції")],
            [KeyboardButton(text="📞 Контакти"), KeyboardButton(text="🐣 Пасхалочка")]
        ],
        resize_keyboard=True
    )
    await message.answer("Головне меню:", reply_markup=keyboard)