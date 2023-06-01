from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from modeus.find_optimal_time import find_optimal
from modeus.modeus import get_rasps
from keyboards.for_singup import get_signup_button
from keyboards.for_work import get_work_buttons
from database_functions import delete_user, check_user

router = Router()  # [1]

@router.message(Text(text='Посмотреть расписание 📚'))  # [2]
async def check_lessions(message: Message):
    fullname = check_user(message.from_user.id)
    rasp = get_rasps(fullname)
    await message.answer(
        rasp,
        reply_markup=get_work_buttons()
    )

@router.message(Text(text='Посмотреть сходства пар друзей 🤝'))  # [2]
async def check_friends_lessions(message: Message):
    await message.answer(
        "Введите ФИО ваших друзей через запятую с помощью команды /f\n\nНапример:\n/f Иванов Иван Иванович, Павлов Павел Павлович",
        reply_markup=get_work_buttons()
    )

@router.message(Text(text='Удалить своё ФИО 😞'))  # [2]
async def unsignup_user(message: Message):
    fullname = check_user(message.from_user.id)
    if fullname:
        delete_user(message.from_user.id)
        await message.answer('Ваше ФИО успешно удалено', reply_markup=get_signup_button())
    else:
        await message.answer('Вашего ФИО и так нет в базе данных', reply_markup=get_signup_button())

@router.message(F.text.startswith('/f'))  # [2]
async def check_friends(message: Message):
    text = message.text[3:]
    fullname = check_user(message.from_user.id)
    friends_fullnames = text.split(',')
    optimal = find_optimal(fullname, friends_fullnames)

    await message.answer(
        optimal,
        reply_markup=get_work_buttons()
    )

@router.message(F.text)  # [2]
async def empty_message(message: Message):
    fullname = check_user(message.from_user.id)
    if fullname:
        await message.answer('Не понимаю вас', reply_markup=get_work_buttons())
    else:
        await message.answer('Вашего ФИО нет в базе данных, нужно добавить', reply_markup=get_signup_button())