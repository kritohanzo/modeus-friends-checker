from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from modeus.modeus import get_json_id
from keyboards.for_singup import get_signup_button
from keyboards.for_work import get_work_buttons
from database_functions import check_user, add_user
from aiogram.filters import Filter

router = Router()  # [1]


class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    await message.answer(
        message.from_user.id,
        reply_markup=get_signup_button()
    )

@router.message(Text(text='Указать своё ФИО 😊'))  # [2]
async def signup_user(message: Message):
    fullname = check_user(message.from_user.id)
    if fullname:
        await message.answer("Вы уже есть в базе данных, приятного пользования!", reply_markup=get_work_buttons())
    else:
        await message.answer(
            "Введите ваше ФИО с помощью команды /my\n\nНапример:\n/my Иванов Иван Иванович",
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(F.text.startswith('/my'))
async def answer_fullname(message: Message):
    text = message.text[4:]
    print(text.split(' '))
    if check_user(message.from_user.id):
        await message.answer("Ах вы обманщик, вы не сможете сломать мне БД", reply_markup=get_work_buttons())
    elif len(text.split(' ')) != 3:
        await message.answer("Мне кажется вы неправильно ввели ФИО", reply_markup=get_work_buttons())
    else:
        try:
            get_json_id(text)
            add_user(message.from_user.id, text)
            await message.answer("Ура, вы в базе данных", reply_markup=get_work_buttons())
        except:
            await message.answer("Такого ФИО нет, попробуй еще раз", reply_markup=ReplyKeyboardRemove())