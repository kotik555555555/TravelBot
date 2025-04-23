from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="💲 Ціна(за зростанням) ↑", callback_data="btn_asc"),
            InlineKeyboardButton(text="💲 Ціна(за спаданням) ↓", callback_data="btn_desc")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="btn_back")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_inline_keyboard2() -> InlineKeyboardMarkup:
    keyboard2 = [
        [
            InlineKeyboardButton(text="🔍 Пошук за назвою міста", callback_data="btn_2.1"),
            InlineKeyboardButton(text="🔙 Назад", callback_data="btn_2.2")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard2)

def get_inline_keyboard3() -> InlineKeyboardMarkup:
    keyboard3 = [
        [
            InlineKeyboardButton(text="✏️ Опишіть ваше замовлення", callback_data="btn_3.1"),
            InlineKeyboardButton(text="🔙 Назад", callback_data="btn_3.2")
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard3)

def get_inline_keyboard4() -> InlineKeyboardMarkup:
    keyboard4 = [
        [
            InlineKeyboardButton(text="🔽 Виберіть спосіб сортування:", callback_data="btn_4.1"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard4)

def get_inline_keyboard5() -> InlineKeyboardMarkup:
    keyboard5 = [
        [
            InlineKeyboardButton(text="📧 Контакти (повідомлення)", callback_data="btn_5.1"),
            InlineKeyboardButton(text="🔙 Назад", callback_data="btn_5.2")
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard5)

def get_inline_keyboard6() -> InlineKeyboardMarkup:
    keyboard6 = [
        [
            InlineKeyboardButton(text="✅ Так", callback_data="btn_yes"),
            InlineKeyboardButton(text="❌ Ні", callback_data="btn_no")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="btn_6.3")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard6)

def get_inline_keyboard1():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔼 Сортувати за зростанням", callback_data="btn_asc")],
        [InlineKeyboardButton(text="🔽 Сортувати за спаданням", callback_data="btn_desc")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="btn_back")]
    ])
    return keyboard

def get_sorting_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬆️ За зростанням", callback_data="sort_asc")],
        [InlineKeyboardButton(text="⬇️ За спаданням", callback_data="sort_desc")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="sort_back")]
    ])
    return keyboard