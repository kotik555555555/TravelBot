import json
import html  # використовується для екранування HTML символів

from aiogram import types, Router
from aiogram.types import FSInputFile, InlineKeyboardButton

# Імпортуємо всі необхідні клавіатури
from keyboards.inline_keyboards import (
    get_inline_keyboard, get_inline_keyboard2, get_inline_keyboard3,
    get_inline_keyboard4, get_inline_keyboard5, get_inline_keyboard6
)

router = Router()  # Створення об'єкта маршрутизатора для обробки повідомлень

# Завантаження даних з JSON-файлу
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Функція створює кнопку бронювання
def get_book_button(offer_title):
    return InlineKeyboardButton(text="Забронювати", callback_data=f"book_{offer_title}")

# Обробник для команди "Готові пропозиції"
@router.message(lambda message: message.text.startswith("🎉 Готові пропозиції"))
async def test_handler(message: types.Message):
    # Отримуємо всі пропозиції з усіх міст
    all_offers = [
        (city.get("name"), offer.get("title"), offer.get("price"), offer.get("description"), offer.get("image"))
        for city in data.get("cities", []) if isinstance(city, dict)
        for offer in city.get("offers", []) if isinstance(offer, dict)
    ]

    if not all_offers:
        await message.answer("❌ Наразі немає доступних пропозицій.", reply_markup=get_inline_keyboard())
        return

    offer_texts = ""

    # Формуємо текст для кожної пропозиції
    for city_name, title, price, description, image in all_offers:
        city_name = html.escape(str(city_name or "Невідоме місто"))
        title = html.escape(str(title or "Без назви"))
        price = html.escape(str(price or "Не вказано"))
        description = html.escape(str(description or "Без опису"))

        offer_text = (
            f"📍 <b>{city_name}</b>: <b>{title}</b>\n"
            f"💰 <b>Ціна:</b> {price} грн\n"
            f"📖 {description}\n"
        )

        if image:
            offer_text += f'🖼️ <a href="{html.escape(image, quote=True)}">Фото пропозиції</a>\n'

        offer_texts += offer_text + "\n\n"

    offer_texts = offer_texts.strip()

    # Якщо текст вміщується в одне повідомлення — надсилаємо
    if len(offer_texts) <= 4096:
        await message.answer(offer_texts, parse_mode="HTML")
    else:
        # Інакше — розбиваємо на частини
        messages = []
        current = ""
        for block in offer_texts.split("\n\n"):
            if len(current) + len(block) + 2 <= 4096:
                current += block + "\n\n"
            else:
                messages.append(current.strip())
                current = block + "\n\n"
        if current:
            messages.append(current.strip())

        for msg in messages:
            await message.answer(msg, parse_mode="HTML")

    # Відправляємо клавіатуру з кнопками
    await message.answer("📋 Оберіть дію:", reply_markup=get_inline_keyboard())

# Обробник повідомлення про міста
@router.message(lambda message: message.text == "🏙️ Пропозиції по містам")
async def test_handler(message: types.Message):
    await message.answer(
        "🔎 Введіть назву міста, щоб знайти події в ньому:",
        reply_markup=get_inline_keyboard2()
    )

# Обробник для розділу бронювання
@router.message(lambda message: message.text == "🛏️ Бронювання")
async def test_handler(message: types.Message):
    await message.answer(
        "📋 Тут можна зробити бронювання.\n🖊️ Напишіть, що саме ви хочете забронювати:",
        reply_markup=get_inline_keyboard3()
    )

# Обробник для перегляду акцій
@router.message(lambda message: message.text == "🎈 Акції")
async def test_handler(message: types.Message):
    # Фільтруємо лише пропозиції зі знижками
    offers_with_discount = [
        offer
        for city in data.get("cities", [])
        if isinstance(city, dict)
        for offer in city.get("offers", [])
        if isinstance(offer, dict) and "discount" in offer
    ]

    if offers_with_discount:
        offer_texts = ""
        for offer in offers_with_discount:
            offer_text = (
                f"🏝 *{offer['title']}*\n"
                f"💰 *Ціна:* {offer['price']} грн\n"
                f"🎉 *Знижка:* {offer['discount']}%\n"
                f"📖 *Опис:* {offer['description']}\n"
            )
            if "image" in offer and offer["image"]:
                offer_text += f"🖼️ [Фото пропозиції]({offer['image']})\n"

            offer_texts += offer_text + "\n\n"

        offer_texts = offer_texts.strip()

        if len(offer_texts) <= 4096:
            await message.answer(offer_texts, reply_markup=get_inline_keyboard4(), parse_mode="Markdown")
        else:
            for i in range(0, len(offer_texts), 4096):
                await message.answer(offer_texts[i:i + 4096], reply_markup=get_inline_keyboard4(), parse_mode="Markdown")
    else:
        await message.answer("🔸 Наразі немає доступних акцій.", reply_markup=get_inline_keyboard4())

# Обробник повідомлення з контактами
@router.message(lambda message: message.text == "📞 Контакти")
async def test_handler(message: types.Message):
    await message.answer(
        "📬 Тут ви можете знайти контакти розробника.\n👇 Натисніть кнопку, щоб дізнатися більше:",
        reply_markup=get_inline_keyboard5()
    )

# Обробник "пасхалки"
@router.message(lambda message: message.text == "🐣 Пасхалочка")
async def test_handler(message: types.Message):
    # Відправка фото (пасхалки)
    photo = FSInputFile("assets/playboi-carti-gq-december-january-2021-02.jpg")
    await message.answer_photo(photo, caption="Ось ваша пасхалочка! 🐣")

    user = message.from_user
    chat = message.chat

    # Формування тексту з інформацією про користувача та чат
    user_info = (
        f"👤 *Дані користувача*\n"
        f"🆔 ID: `{user.id}`\n"
        f"👤 First name: {user.first_name or '—'}\n"
        f"👥 Last name: {user.last_name or '—'}\n"
        f"💬 Username: @{user.username if user.username else 'Немає'}\n"
        f"🌐 Language: {user.language_code or '—'}\n"
        f"👑 Premium: {'✅ Так' if getattr(user, 'is_premium', False) else '❌ Ні'}\n"
        f"🤖 Is bot: {'✅' if user.is_bot else '❌'}\n"
        f"👥 Can join groups: {getattr(user, 'can_join_groups', '—')}\n"
        f"📖 Can read all group messages: {getattr(user, 'can_read_all_group_messages', '—')}\n"
        f"🔍 Supports inline queries: {getattr(user, 'supports_inline_queries', '—')}\n\n"

        f"💬 *Інформація про чат (повідомлення надіслано у)*\n"
        f"📌 Chat type: {chat.type}\n"
        f"🏷️ Chat title: {chat.title or '—'}\n"
        f"👥 Chat ID: `{chat.id}`\n"
        f"👤 Chat username: @{chat.username if chat.username else 'Немає'}\n"
        f"👥 Is forum: {'✅' if getattr(chat, 'is_forum', False) else '❌'}\n\n"

        f"📨 *Повідомлення*\n"
        f"🆔 Message ID: {message.message_id}\n"
        f"⏰ Дата: {message.date}\n"
        f"🧷 Reply to message: {'Так' if message.reply_to_message else 'Ні'}\n"
        f"📎 Є медіа: {'Так' if message.photo or message.document or message.video else 'Ні'}"
    )

    await message.answer(user_info, parse_mode="Markdown")
    await message.answer("👀 Це *точно* твої дані, чи не так?", reply_markup=get_inline_keyboard6())