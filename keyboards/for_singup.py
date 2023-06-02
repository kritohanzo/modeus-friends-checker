from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyCallback(CallbackData, prefix="my"):
    action: str


def get_signup_button():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Указать своё ФИО 😊",
        callback_data=MyCallback(action="signup").pack(),
    )
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
