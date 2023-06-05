from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from database.database_functions import check_user, delete_user
from keyboards.for_singup import get_signup_button
from keyboards.for_work import (
    get_backs, get_friends_today_or_tomorrow_buttons,
    get_me_today_or_tomorrow_buttons, get_work_buttons,
)
from modeus.find_optimal_time import find_optimal
from modeus.modeus import get_rasps


router = Router()


class MyCallback(CallbackData, prefix="my"):
    action: str


@router.callback_query(MyCallback.filter(F.action == "get_me_schedule"))
async def check_lessions(callback_query):
    if not check_user(callback_query.from_user.id):
        await callback_query.message.answer(
            "Вашего ФИО нет в базе данных. Чтобы я мог работать - его нужно добавить.",
            reply_markup=get_signup_button(),
        )
    else:
        await callback_query.message.answer(
            "На сегодня или на завтра?",
            reply_markup=get_me_today_or_tomorrow_buttons(),
    )


@router.callback_query(MyCallback.filter(F.action == "get_me_today"))
async def check_me_today_lessions(callback_query):
    if not check_user(callback_query.from_user.id):
        await callback_query.message.answer(
            "Вашего ФИО нет в базе данных. Чтобы я мог работать - его нужно добавить.",
            reply_markup=get_signup_button(),
        )
    else:
        msg = await callback_query.message.answer(
            "Происходит выгрузка расписания, пожалуйста, подождите 🙂"
        )
        fullname = check_user(callback_query.from_user.id)
        rasp = get_rasps(fullname)
        await msg.edit_text(rasp, reply_markup=get_work_buttons())


@router.callback_query(MyCallback.filter(F.action == "get_me_tomorrow"))
async def check_me_tomorrow_lessions(callback_query):
    if not check_user(callback_query.from_user.id):
        await callback_query.message.answer(
            "Вашего ФИО нет в базе данных. Чтобы я мог работать - его нужно добавить.",
            reply_markup=get_signup_button(),
        )
    else:
        msg = await callback_query.message.answer(
            "Происходит выгрузка расписания, пожалуйста, подождите 🙂"
        )
        fullname = check_user(callback_query.from_user.id)
        rasp = get_rasps(fullname, tomorrow=True)
        await msg.edit_text(rasp, reply_markup=get_work_buttons())


@router.callback_query(
    MyCallback.filter(F.action == "get_similarities")
)
async def check_friends_lessions(callback_query):
    if not check_user(callback_query.from_user.id):
        await callback_query.message.answer(
            "Вашего ФИО нет в базе данных. Чтобы я мог работать - его нужно добавить.",
            reply_markup=get_signup_button(),
        )
    else:
        await callback_query.message.answer(
            "На сегодня или на завтра?",
            reply_markup=get_friends_today_or_tomorrow_buttons(),
        )


@router.callback_query(MyCallback.filter(F.action == "get_friends_today"))
async def check_friends_lessions_today(callback_query):
    if not check_user(callback_query.from_user.id):
        await callback_query.message.answer(
            "Вашего ФИО нет в базе данных. Чтобы я мог работать - его нужно добавить.",
            reply_markup=get_signup_button(),
        )
    else:
        await callback_query.message.answer(
            "Введите ФИО ваших друзей через запятую с помощью команды /ftd\n\n"
            "Например:\n/ftd Иванов Иван Иванович, Павлов Павел Павлович",
            reply_markup=get_backs(),
        )


@router.callback_query(MyCallback.filter(F.action == "get_friends_tomorrow"))
async def check_friends_lessions_tomorrow(callback_query):
    if not check_user(callback_query.from_user.id):
        await callback_query.message.answer(
            "Вашего ФИО нет в базе данных. Чтобы я мог работать - его нужно добавить.",
            reply_markup=get_signup_button(),
        )
    else:
        await callback_query.message.answer(
            "Введите ФИО ваших друзей через запятую с помощью команды /ftm\n\n"
            "Например:\n/ftm Иванов Иван Иванович, Павлов Павел Павлович",
            reply_markup=get_backs(),
        )


@router.callback_query(MyCallback.filter(F.action == "delete_fullname"))  # [2]
async def unsignup_user(callback_query):
    fullname = check_user(callback_query.from_user.id)
    if fullname:
        delete_user(callback_query.from_user.id)
        await callback_query.message.answer(
            "Ваше ФИО успешно удалено 😞", reply_markup=get_signup_button()
        )
    else:
        await callback_query.message.answer(
            "Вашего ФИО и так нет в базе данных.",
            reply_markup=get_signup_button(),
        )


@router.callback_query(MyCallback.filter(F.action == "get_back"))
async def get_back(callback_query):
    await callback_query.message.answer(
        "И снова здравствуйте, что вы хотите проверить на этот раз?", reply_markup=get_work_buttons()
    )


@router.message(F.text.startswith("/ftd"))  # [2]
async def check_friends(message):
    text = message.text[5:]
    print(text)
    if ',' not in text and len(text.split(' ')) > 3:
        await message.answer(
            "Кажется, вы ошиблись при вводе. Убедитесь, что перечислили ФИО через запятую.",
            reply_markup=get_backs(),
        )
    else:
        msg = await message.answer(
            "Происходит сравнение расписаний, пожалуйста, подождите."
        )
        fullname = check_user(message.from_user.id)
        friends_fullnames = text.split(",")
        optimal = find_optimal(fullname, friends_fullnames, tomorrow=False)

        await msg.edit_text(optimal, reply_markup=get_work_buttons())


@router.message(F.text.startswith("/ftm"))  # [2]
async def check_friends(message):
    text = message.text[5:]
    print(text)
    if ',' not in text and len(text.split(' ')) > 3:
        await message.answer(
            "Кажется, вы ошиблись при вводе. Убедитесь, что перечислили ФИО через запятую.",
            reply_markup=get_backs(),
        )
    else:
        msg = await message.answer(
            "Происходит сравнение расписаний, пожалуйста, подождите."
        )
        fullname = check_user(message.from_user.id)
        friends_fullnames = text.split(",")
        optimal = find_optimal(fullname, friends_fullnames, tomorrow=True)

        await msg.edit_text(optimal, reply_markup=get_work_buttons())


@router.message(F.text)  # [2]
async def empty_message(message):
    fullname = check_user(message.from_user.id)
    if fullname:
        await message.answer(
            "Кажется, вы ввели несуществующую команду.",
            reply_markup=get_work_buttons(),
        )
    else:
        await message.answer(
            "Вашего ФИО нет в базе данных. Чтобы я мог работать - его нужно добавить.",
            reply_markup=get_signup_button(),
        )
