from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_reply_kb() -> ReplyKeyboardMarkup:

    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Мои Заявки"))
    builder.row(KeyboardButton(text="Профиль"), KeyboardButton(text="Помощь"))

    return builder.as_markup(
        resize_keyboard=True, input_field_placeholder="Выберите действие..."
    )


def get_auth_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Вход по email"))
    return builder.as_markup(resize_keyboard=True)
