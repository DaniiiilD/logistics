from aiogram import Router, F, types
from src.api.handlers.user import UserService

router = Router()


@router.message(F.text == "Профиль")
async def show_profile(message: types.Message, user_service: UserService):
    await message.delete()

    user = await user_service.get_user_by_tg_id(message.from_user.id)
    if user and user.driver:
        await message.answer(
            f"Ваш прифиль:\n"
            f"ФИО: {user.driver.full_name}\n"
            f"Телефон: {user.driver.phone}\n"
            f"Трансопрт: {user.driver.transport_type}"
        )
    else:
        await message.answer("Профиль не найден. Пожалуйста авторизуйтесь!")


@router.message(F.text == "Помощь")
async def show_help(message: types.Message):
    await message.delete()
    await message.answer("Здесь будет помощь по навигации и работе с заказами.")


@router.callback_query(F.data == "main_menu")
async def main_menu_rollback(callback: types.CallbackQuery, user_service: UserService):

    user = await user_service.get_user_by_tg_id(callback.from_user.id)

    await callback.message.edit_text(
        f"Главное меню. \nС возвращением, {user.driver.full_name}!", reply_markup=None
    )

    await callback.answer()
