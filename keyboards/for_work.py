from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyCallback(CallbackData, prefix="my"):
    action: str


def get_work_buttons():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Посмотреть расписание 📚",
        callback_data=MyCallback(action="get_me_schedule").pack(),
    )
    kb.button(
        text="Посмотреть сходства пар друзей 🤝",
        callback_data=MyCallback(action="get_similarities").pack(),
    )
    kb.button(
        text="Удалить своё ФИО 😞",
        callback_data=MyCallback(action="delete_fullname").pack(),
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_me_today_or_tomorrow_buttons():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="На сегодня",
        callback_data=MyCallback(action="get_me_today").pack(),
    )
    kb.button(
        text="На завтра",
        callback_data=MyCallback(action="get_me_tomorrow").pack(),
    )
    kb.button(text="Назад", callback_data=MyCallback(action="get_back").pack())
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_friends_today_or_tomorrow_buttons():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="На сегодня",
        callback_data=MyCallback(action="get_friends_today").pack(),
    )
    kb.button(
        text="На завтра",
        callback_data=MyCallback(action="get_friends_tomorrow").pack(),
    )
    kb.button(text="Назад", callback_data=MyCallback(action="get_back").pack())
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_backs():
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data=MyCallback(action="get_back").pack())
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
