from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_work_buttons() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Посмотреть расписание 📚')
    kb.button(text='Посмотреть сходства пар друзей 🤝')
    kb.button(text='Удалить своё ФИО 😞')
    return kb.as_markup(resize_keyboard=True)