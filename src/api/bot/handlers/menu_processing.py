from aiogram import Router, F, types
from src.api.handlers.user import UserService
from src.api.bot.utils.decorators import delete_user_message
from src.api.bot.utils.messages import BotMessages

router = Router()


@router.message(F.text == "Профиль")
@delete_user_message
async def show_profile(message: types.Message, user_service: UserService):

    user = await user_service.get_user_by_tg_id(message.from_user.id)
    if user and user.driver:
        await message.answer(
            BotMessages.Menu.PROFILE.format(
                full_name=user.driver.full_name,
                phone=user.driver.phone,
                transport_type=user.driver.transport_type
            )
        )
    else:
        await message.answer(BotMessages.Menu.NOT_FOUND)


@router.message(F.text == "Помощь")
@delete_user_message
async def show_help(message: types.Message):
    await message.answer(BotMessages.Menu.HELP)


@router.callback_query(F.data == "main_menu")
async def main_menu_rollback(callback: types.CallbackQuery, user_service: UserService):

    user = await user_service.get_user_by_tg_id(callback.from_user.id)

    await callback.message.edit_text(
        f"Главное меню. \nС возвращением, {user.driver.full_name}!", reply_markup=None
    )

    await callback.answer()
