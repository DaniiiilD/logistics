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

router = Router()


@router.message(F.text == "Мои Заявки")
async def show_orders_menu(
    message: types.Message,
    order_service: OrderService,
    user_service: UserService,
    state: FSMContext,
):
    await message.delete()

    data = await state.get_data()
    if last_id := data.get("last_msg_id"):
        try:
            await message.bot.delete_message(message.chat.id, last_id)
        except:
            pass

    user = await user_service.get_user_by_tg_id(message.from_user.id)
    driver_transport = user.driver.transport_type

    orders, total_pages = await order_service.get_orders_for_bot(
        transport_type=driver_transport, page=0
    )

    if not orders:
        msg = await message.answer("Активных заявок пока нет.")
    else:
        msg = await message.answer(
            "*Список доступных заявок:*",
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
        "*Список доступных заявок:*",
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
        await callback.answer("Заказ больше не актуален", show_alert=True)
        return

    detail_text = (
        f"*Заказ №{order.id}*\n\n"
        f"*Отправитель:* {order.company.company_name}\n"
        f"*Тип авто:* {order.transport_type}\n"
        f"*Даты доставки:* {order.from_date.strftime('%d.%m.%y')} - {order.to_date.strftime('%d.%m.%y')}\n"
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

    confirm_text = f"*Вы увернеы что хотите откликнуться на заказ №{order_id}*"

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
        await callback.answer("Ошибка: пользователь не найден.")
        return

    try:
        await offer_service.create_offer(user_id=user.id, order_id=order_id)
        await callback.message.edit_text(
            f"*Заявка на заказ №{order_id} успешно отправлена!*\n\n"
            "Компания получила ваше уведомление. Если вас выберут, бот пришлет сообщение.",
            parse_mode="Markdown",
        )
    except HTTPException as e:
        await callback.message.answer(f"{e.detail}")
    except Exception:
        await callback.message.answer("Произошла ошибка при отправке заявки.")

    await callback.answer()
