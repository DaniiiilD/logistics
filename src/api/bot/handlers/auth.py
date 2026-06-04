from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from src.api.bot.utils.state import AuthState
from src.api.handlers.user import UserService
from pydantic import TypeAdapter, EmailStr, ValidationError
from src.api.bot.keyboards.reply_kb import get_main_reply_kb
from src.api.bot.utils.decorators import delete_user_message
from src.api.bot.utils.messages import BotMessages
from aiogram.exceptions import TelegramBadRequest
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "Вход по email")
@delete_user_message
async def login_start(message: types.Message, state: FSMContext):

    data = await state.get_data()
    if last_id := data.get("last_msg_id"):
        try:
            await message.bot.delete_message(message.chat.id, last_id)
        except TelegramBadRequest as e:
            logger.debug(f"Не удалось удалить сообщение: {e.message}")
        except Exception as e:
            logger.error(f'Критическая ошибка при удалении сообщения', exc_info=True)

    await state.set_state(AuthState.waiting_for_email)
    await state.update_data(auth_mode="login")
    await message.answer(BotMessages.AUTH.ENTER_EMAIL)


@router.message(AuthState.waiting_for_email)
async def process_email(
    message: types.Message, state: FSMContext, user_service: UserService
):
    email = message.text.lower().strip()

    try:
        TypeAdapter(EmailStr).validate_python(email)
    except ValidationError:
        await message.answer(BotMessages.AUTH.INVALID_EMAIL)
        return

    user = await user_service.get_user_by_email(email)
    if not user:
        await message.answer(BotMessages.AUTH.USER_NOT_FOUND)
        return

    await user_service.send_login_code(email)
    await state.update_data(email=email)
    await state.set_state(AuthState.waiting_for_code)
    await message.answer(BotMessages.AUTH.CODE_SENT)


@router.message(AuthState.waiting_for_code)
async def process_code(
    message: types.Message, state: FSMContext, user_service: UserService
):
    code = message.text.strip()
    data = await state.get_data()
    email = data.get("email")

    success = await user_service.vetify_login_user(
        email=email, code=code, telegram_id=message.from_user.id
    )

    if success:
        await state.clear()
        await message.answer(BotMessages.AUTH.SUCCESS, reply_markup=get_main_reply_kb())
    else:
        await message.answer(BotMessages.AUTH.INVALID_CODE)
