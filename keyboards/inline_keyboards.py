from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Ціна(за зростанням)", callback_data="btn_asc"),
            InlineKeyboardButton(text="Ціна(за спаданням)", callback_data="btn_esc")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="btn_back")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_inline_keyboard2() -> InlineKeyboardMarkup:
    keyboard2 = [
        [
            InlineKeyboardButton(text="Ціна(за зростанням)", callback_data="btn_2.1"),
            InlineKeyboardButton(text="Ціна(за спаданням)", callback_data="btn_2.2")
        ],
        [
            InlineKeyboardButton(text="Пошук за назвою міста", callback_data="btn_2.3"),
            InlineKeyboardButton(text="Назад", callback_data="btn_2.4")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard2)

def get_inline_keyboard3() -> InlineKeyboardMarkup:
    keyboard3 = [
        [
            InlineKeyboardButton(text="Опишіть ваше замовлення", callback_data="btn_3.1"),
            InlineKeyboardButton(text="Назад", callback_data="btn_3.2")
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard3)

def get_inline_keyboard4() -> InlineKeyboardMarkup:
    keyboard4 = [
        [
            InlineKeyboardButton(text="Забронювати", callback_data="btn_4.1"),
            InlineKeyboardButton(text="Назад", callback_data="btn_4.2")
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard4)

def get_inline_keyboard5() -> InlineKeyboardMarkup:
    keyboard5 = [
        [
            InlineKeyboardButton(text="Контакти (повідомлення)", callback_data="btn_5.1"),
            InlineKeyboardButton(text="Назад", callback_data="btn_5.2")
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard5)
