from aiogram import types, Router
from aiogram.types import FSInputFile

from keyboards.inline_keyboards import get_inline_keyboard, get_inline_keyboard2, get_inline_keyboard3, \
    get_inline_keyboard4, get_inline_keyboard5

router = Router()


@router.message(lambda message: message.text == "Готові пропозиції")
async def test_handler(message: types.Message):
    await message.answer("""Тут є всі готові пропозиції які є на даний момент.""", reply_markup=get_inline_keyboard())


@router.message(lambda message: message.text == "Пропозиції по містам")
async def test_handler(message: types.Message):
    await message.answer("""Введіть місто щоб знайти події в ньому:""", reply_markup=get_inline_keyboard2())


@router.message(lambda message: message.text == "Бронювання")
async def test_handler(message: types.Message):
    await message.answer("""Тут можна забронювати щось наперед. Напишіть те що ви забронювали:""", reply_markup=get_inline_keyboard3())


@router.message(lambda message: message.text == "Акції")
async def test_handler(message: types.Message):
    await message.answer("""Тут є всі акції на даний момент.""", reply_markup=get_inline_keyboard4())


@router.message(lambda message: message.text == "Контакти")
async def test_handler(message: types.Message):
    await message.answer("""Тут є контакти розробника.Нажми на кнопку щоб дізнатися їх.""",
                         reply_markup=get_inline_keyboard5())


@router.message(lambda message: message.text == "Пасхалочка")
async def test_handler(message: types.Message):
    photo = FSInputFile(r"C:\Users\asus\Documents\GitHub\TravelBot\assets\playboi-carti-gq-december-january-2021-02.jpg")  # Замініть шлях на реальний шлях до зображення
    await message.answer_photo(photo, caption="Ось ваша пасхалочка! 🐣")
