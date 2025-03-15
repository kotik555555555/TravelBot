from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard()-> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text="Готові пропозиції"), KeyboardButton(text="Пропозиції по містам")],
            [KeyboardButton(text="Бронювання"), KeyboardButton(text="Акції")],
            [KeyboardButton(text="Контакти"), KeyboardButton(text="Пасхалочка")]
        ],
        resize_keyboard=True
    )
    return keyboard