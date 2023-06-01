from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_signup_button() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Указать своё ФИО 😊')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
