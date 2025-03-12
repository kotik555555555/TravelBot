from aiogram import types, Router

router = Router()

@router.message(lambda message: message.text == "Test")
async def test_handler(message: types.Message):
    await message.answer("""It's test message!""")