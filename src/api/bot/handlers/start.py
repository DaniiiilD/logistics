from aiogram import Router, types
from aiogram.filters import CommandObject, CommandStart
from src.api.handlers.user import UserService
from src.api.bot.keyboards.reply_kb import get_main_reply_kb, get_auth_kb
from src.core.constants import Role

router = Router()


@router.message(CommandStart())
async def cmd_start(
    message: types.Message, command: CommandObject, user_service: UserService
):
    await message.delete()

    user = await user_service.get_user_by_tg_id(message.from_user.id)

    if command.args:
        try:
            await user_service.link_telegram_account(command.args, message.from_user.id)
            user = await user_service.get_user_by_tg_id(message.from_user.id)
            await message.answer("Аккаунт успешно привязан!")
        except ValueError as e:
            await message.answer(f"Ошибка: {str(e)}")

    if user:
        if user.role != Role.DRIVER.value:
            await message.answer(
                "Доступ Запрещен. Этот бот прднаазначен для водителей."
            )
            return
        await message.answer(
            f"С возвращением, {user.driver.full_name if user.driver else 'Водитель'}!",
            reply_markup=get_main_reply_kb(),
        )
    else:
        await message.answer(
            "Добро пожаловать! Пожалуйста, авторизуйтеся для работы.",
            reply_markup=get_auth_kb(),
        )
