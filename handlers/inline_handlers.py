from aiogram import types, Router
from keyboards.inline_keyboards import get_inline_keyboard, get_inline_keyboard2, get_inline_keyboard3, get_inline_keyboard4, get_inline_keyboard5

router = Router()

# @router.callback_query(lambda c:  c.data.startswith("test_btn_"))
# async def test_callback_handler(callback_query: types.CallbackQuery):
#     data = callback_query.data
#     if data == "test_btn_1":
#         await callback_query.message.edit_text("Edited")
#         await callback_query.answer("You pressed first inline button")
#     elif data == "test_btn_2":
#         await callback_query.message.delete()
#         await callback_query.message.answer("You pressed second inline button", reply_markup=get_inline_test2())

@router.callback_query(lambda c:  c.data.startswith("btn_1."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_1.1":
        await callback_query.message.answer("Ціна(за зростанням):")
    elif data == "btn_1.2":
        await callback_query.message.answer("Ціна(за зростанням):")