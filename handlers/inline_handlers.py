from aiogram import types, Router
from keyboards.inline_keyboards import get_inline_test2

router = Router()

@router.callback_query(lambda c:  c.data.startswith("test_btn_"))
async def test_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "test_btn_1":
        await callback_query.message.edit_text("Edited")
        await callback_query.answer("You pressed first inline button")
    elif data == "test_btn_2":
        await callback_query.message.delete()
        await callback_query.message.answer("You pressed second inline button", reply_markup=get_inline_test2())

@router.callback_query(lambda c:  c.data.startswith("btn_"))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_1":
        await callback_query.message.answer("Пропозиції в Дрогобичу:")
    elif data == "btn_2":
        await callback_query.message.answer("Пропозиції в Стрию:")
    elif data == "btn_3":
        await callback_query.message.answer("Пропозиції в Бориславі:")
    elif data == "btn_4":
        await callback_query.message.answer("Пропозиції в Трускавці:")