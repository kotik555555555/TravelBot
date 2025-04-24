import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# keyboards
from keyboards.reply_keyboards import get_main_keyboard
from handlers import register_handlers


TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()
register_handlers(dp)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"""Привіт, {html.bold(message.from_user.full_name)}! 
👋 Ласкаво просимо до нашого бота!

Цей бот створений, щоб зробити ваше життя простішим і цікавішим! Тут ви знайдете:

✨ Персоналізовані привітання: Кожен користувач отримує тепле вітання з ім'ям! 

🗂️ Головне меню: Легкий доступ до всіх функцій бота. 

📅 Актуальні новини: Будьте в курсі останніх подій та акцій. 

❓ Допомога: Швидкі відповіді на ваші запитання.

Давайте розпочнемо цю подорож разом! 🚀""", reply_markup=get_main_keyboard())


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    # And the run events dispatching
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())