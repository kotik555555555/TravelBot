from aiogram import types, Router

router = Router()

@router.message(lambda message: message.text == "Готові пропозиції")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""")

@router.message(lambda message: message.text == "Пропозиції по містам")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""")

@router.message(lambda message: message.text == "Бронювання")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""")

@router.message(lambda message: message.text == "Акції")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""")

@router.message(lambda message: message.text == "Контакти")
async def test_handler(message: types.Message):
    await message.answer("""В процесі""")