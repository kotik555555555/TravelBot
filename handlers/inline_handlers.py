from aiogram import types, Router
from keyboards.reply_keyboards  import get_main_keyboard

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
        await callback_query.message.answer("Ціна(за спаданням):")
    elif data == "btn_1.3":
        await callback_query.message.answer("В процесі...")

@router.callback_query(lambda c:  c.data.startswith("btn_2."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_2.1":
        await callback_query.message.answer("Ціна(за зростанням):")
    elif data == "btn_2.2":
        await callback_query.message.answer("Ціна(за спаданням):")
    elif data == "btn_2.3":
        await callback_query.message.answer("Введіть назву міста:")
    elif data == "btn_2.4":
        await callback_query.message.answer("В процесі...")

@router.callback_query(lambda c:  c.data.startswith("btn_3."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_3.1":
        await callback_query.message.answer("Опишіть ваше замовлення:")
    elif data == "btn_3.2":
        await callback_query.message.answer("В процесі...")

@router.callback_query(lambda c:  c.data.startswith("btn_4."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_4.1":
        await callback_query.message.answer("Список акцій:")
    elif data == "btn_4.2":
        await callback_query.message.answer("В процесі...")

@router.callback_query(lambda c:  c.data.startswith("btn_5."))
async def city_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "btn_5.1":
        await callback_query.message.answer("Потім напишу.")
    elif data == "btn_5.2":
        await callback_query.message.answer("В процесі...")