from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardRemove
from database.database_functions import add_user, check_user
from keyboards.for_singup import get_signup_button
from keyboards.for_work import get_work_buttons
from modeus.modeus import get_json_id


router = Router()


class MyCallback(CallbackData, prefix="my"):
    action: str


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    await message.answer(
        "Привет, я бот, который может смотреть ваше расписание "
        "и сопоставлять его с расписанием ваших друзей. "
        "Благодаря мне, вы сможете узнать, когда вам с друзьями "
        "будет удобно встретиться после или между пар!\n\n"
        "Если вы заметите какие-то баги - обратитесь "
        "к разработчику бота «@kritohanzo»\n\n"
        "Чтобы начать пользоваться мной - вам нужно указать "
        "своё ФИО. Его можно будет удалить в любой момент.",
        reply_markup=get_signup_button(),
    )


@router.callback_query(MyCallback.filter(F.action == "signup"))
async def handle(callback_query):
    fullname = check_user(callback_query.from_user.id)
    if fullname:
        await callback_query.message.answer(
            "Вы уже есть в базе данных, приятного пользования 😉",
            reply_markup=get_work_buttons(),
        )
    else:
        await callback_query.message.answer(
            "Введите ваше ФИО с помощью команды /me\n\nНапример:\n/me Иванов Иван Иванович",
            reply_markup=ReplyKeyboardRemove(),
        )


@router.message(F.text.startswith("/me"))
async def answer_fullname(message: Message):
    text = message.text[4:]
    if check_user(message.from_user.id):
        await message.answer(
            "Вы уже есть в базе данных, приятного пользования 😉",
            reply_markup=get_work_buttons(),
        )
    elif len(text.split(" ")) != 3:
        await message.answer(
            "Мне кажется вы неправильно ввели ФИО, попробуйте ввести ФИО ещё раз 🤔",
            reply_markup=get_work_buttons(),
        )
    else:
        try:
            get_json_id(text)
            add_user(message.from_user.id, text)
            await message.answer(
                "Теперь ваше ФИО находится в базе данных, приятного пользования 😉",
                reply_markup=get_work_buttons(),
            )
        except:
            await message.answer(
                "Такого ФИО нет в модеусе, возможно вы ошиблись? "
                "Попробуйте ввести ФИО ещё раз 🤔",
                reply_markup=ReplyKeyboardRemove(),
            )
