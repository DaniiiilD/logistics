from aiogram import types, F, Router
from src.api.handlers.company.order import OrderService
from src.api.handlers.user import UserService
from src.api.handlers.driver.offer import DriverOfferService
from aiogram.fsm.context import FSMContext
from src.api.bot.keyboards.orders_kb import get_orders_list_kb
from fastapi import HTTPException
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
)
from src.api.bot.utils.decorators import delete_user_message
from src.api.bot.utils.messages import BotMessages
from aiogram.exceptions import TelegramBadRequest
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "Мои Заявки")
@delete_user_message
async def show_orders_menu(
    message: types.Message,
    order_service: OrderService,
    user_service: UserService,
    state: FSMContext,
):

    data = await state.get_data()
    if last_id := data.get("last_msg_id"):
        try:
            await message.bot.delete_message(message.chat.id, last_id)
        except TelegramBadRequest as e:
            logger.debug(f"Не удалось удалить сообщение: {e.message}")
        except Exception as e:
            logger.error(f'Критическая ошибка при удалении сообщения', exc_info=True)

    user = await user_service.get_user_by_tg_id(message.from_user.id)
    driver_transport = user.driver.transport_type

    orders, total_pages = await order_service.get_orders_for_bot(
        transport_type=driver_transport, page=0
    )

    if not orders:
        msg = await message.answer(BotMessages.Orders.NO_ACTIVE)
    else:
        msg = await message.answer(
            BotMessages.Orders.AVAILABLE_LIST,
            reply_markup=get_orders_list_kb(orders, 0, total_pages),
            parse_mode="Markdown",
        )

        await state.update_data(last_msg_id=msg.message_id)


@router.callback_query(F.data.startswith("orders_page:"))
async def process_orders_pagination(
    callback: types.CallbackQuery,
    order_service: OrderService,
    user_service: UserService,
):
    page = int(callback.data.split(":")[1])

    user = await user_service.get_user_by_tg_id(callback.from_user.id)
    orders, total_pages = await order_service.get_orders_for_bot(
        transport_type=user.driver.transport_type, page=page
    )

    await callback.message.edit_text(
        BotMessages.Orders.AVAILABLE_LIST,
        reply_markup=get_orders_list_kb(orders, page, total_pages),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("order_view:"))
async def process_order_view(
    callback: types.CallbackQuery, order_service: OrderService
):

    order_id = int(callback.data.split(":")[1])

    order = await order_service.get_order_with_details_for_drivers(order_id)

    if not order:
        await callback.answer(BotMessages.Orders.OUTDATED, show_alert=True)
        return

    detail_text = BotMessages.Orders.DETAIL.format(
        order_id=order_id,
        company_name=order.company.company_name,
        transport_type=order.transport_type,
        from_date=order.from_date.strftime('%d.%m.%y'),
        to_date=order.to_date.strftime('%d.%m.%y')
    )
    
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="Откликнуться", callback_data=f"order_apply_confirm:{order.id}"
        )
    )

    builder.row(
        InlineKeyboardButton(text="Назад к списку", callback_data="orders_page:0")
    )

    await callback.message.edit_text(
        text=detail_text, reply_markup=builder.as_markup(), parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("order_apply_confirm:"))
async def order_confirm(callback: types.CallbackQuery):

    order_id = int(callback.data.split(":")[1])

    confirm_text = BotMessages.Orders.CONFIRM_APPLY.format(order_id=order_id)

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Да, Отклинкуться", callback_data=f"order_apply_final:{order_id}"
    )

    builder.button(text="Отмена", callback_data=f"order_view:{order_id}")

    builder.adjust(1)

    await callback.message.edit_text(
        text=confirm_text, reply_markup=builder.as_markup(), parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("order_apply_final:"))
async def process_order_apply_final(
    callback: types.CallbackQuery,
    user_service: UserService,
    offer_service: DriverOfferService,
):
    order_id = int(callback.data.split(":")[1])

    user = await user_service.get_user_by_tg_id(callback.from_user.id)

    if not user:
        await callback.answer(BotMessages.Orders.USER_NOT_FOUND)
        return

    try:
        await offer_service.create_offer(user_id=user.id, order_id=order_id)
        await callback.message.edit_text(
            BotMessages.Orders.APPLY_SUCCESS.format(order_id=order_id),
            parse_mode="Markdown",
        )
    except HTTPException as e:
        await callback.message.answer(f"{e.detail}")
    except Exception:
        await callback.message.answer(BotMessages.Orders.APPLY_ERROR)

    await callback.answer()
