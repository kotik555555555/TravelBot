from aiogram import types, Router
from keyboards.inline_keyboards import get_inline_keyboard, get_inline_keyboard2, get_inline_keyboard3, get_inline_keyboard4, get_inline_keyboard5

router = Router()

@router.message(lambda message: message.text == "Готові пропозиції")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""", reply_markup=get_inline_keyboard())

@router.message(lambda message: message.text == "Пропозиції по містам")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""", reply_markup=get_inline_keyboard2())

@router.message(lambda message: message.text == "Бронювання")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""", reply_markup=get_inline_keyboard3())

@router.message(lambda message: message.text == "Акції")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""", reply_markup=get_inline_keyboard4())

@router.message(lambda message: message.text == "Контакти")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""", reply_markup=get_inline_keyboard5())

@router.message(lambda message: message.text == "Пасхалочка")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""")