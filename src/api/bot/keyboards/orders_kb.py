from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_orders_list_kb(orders, page: int, total_pages: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for o in orders:
        builder.button(
            text=f"Заказ №{o.id} | {o.transport_type}",
            callback_data=f"order_view:{o.id}",
        )
    builder.adjust(1)

    back_btn = (
        InlineKeyboardButton(text="<- Назад", callback_data=f"orders_page:{page - 1}")
        if page > 0
        else None
    )

    page_btn = InlineKeyboardButton(
        text=f"{page + 1} / {total_pages}", callback_data="ignore"
    )

    next_btn = (
        InlineKeyboardButton(text="Вперед ->", callback_data=f"orders_page:{page + 1}")
        if page < total_pages - 1
        else None
    )

    builder.row(*[btn for btn in [back_btn, page_btn, next_btn] if btn])
    builder.row(InlineKeyboardButton(text="В главное меню", callback_data="main_menu"))
    return builder.as_markup()
