import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from database_functions import add_user, check_user, delete_user, update_user
from handlers import singup, work

async def main():
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_TOKEN")
    bot = Bot(bot_token)
    dp = Dispatcher()

    dp.include_routers(singup.router)
    dp.include_routers(work.router)    

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



# button_signup_user = KeyboardButton('Указать своё ФИО 😊')
# greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# greet_kb.add(button_signup_user)

# button_check_resp = KeyboardButton('Посмотреть расписание 📚', )
# button_check_friend = KeyboardButton('Посмотреть сходства пар друзей 🤝')
# button_unsignup_user = KeyboardButton('Удалить своё ФИО 😞')
# work_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# work_kb.add(button_check_resp)
# work_kb.add(button_check_friend)
# work_kb.add(button_unsignup_user)

# async def ask_full_name(message):
#     await message.reply('Напиши своё ФИО')

# async def user_no_signup(message):
#     await message.reply('У тебя не указано ФИО, я не могу так работать', reply_markup=greet_kb)

# @dp.message_handler(commands=['start'])
# async def process_start_command(message: types.Message):
    
#     await message.reply("Привет, я очень рад, что ты написал мне!\n\nЯ бот, который может показать тебе твои пары на сегодня или "
#                         "же подсказать, когда ты сможешь встретиться с друзьями между парами, учитывая ваши расписания!\n\n"
#                         "Чтобы воспользоваться мной - мне нужно знать кто ты, нажми на кнопочку внизу.", reply_markup=greet_kb)

# @dp.message_handler()
# async def process_messsage_command(message: types.Message):
#     if message.text == 'Указать своё ФИО 😊':
#         await ask_full_name(message)
#     elif message.text == "Посмотреть расписание 📚":
#         if not check_user(message.from_id):
#             await user_no_signup(message)
#     elif message.text == 'Посмотреть сходства пар друзей 🤝':
#         await ask_full_name(message)
#     else:
#         await message.reply(get_rasps(message.text))
#     print(message.text)


if __name__ == '__main__':
    asyncio.run(main())