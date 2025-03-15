from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_inline_test() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="test1", callback_data="test_btn_1"),
         InlineKeyboardButton(text="test2", callback_data="test_btn_2")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard1 = [
        [
            InlineKeyboardButton(text="Дрогобич", callback_data="btn_1"),
            InlineKeyboardButton(text="Стрий", callback_data="btn_2")
        ],
        [
            InlineKeyboardButton(text="Борислав", callback_data="btn_3"),
            InlineKeyboardButton(text="Трускавець", callback_data="btn_4")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard1)

def get_inline_test2() -> InlineKeyboardMarkup:
    keyboard2 = [
        [InlineKeyboardButton(text="test3", callback_data="test_btn_3"),
         InlineKeyboardButton(text="test4", callback_data="test_btn_4")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard2)