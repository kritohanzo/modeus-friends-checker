import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from modeus import get_json_id, get_rasps


load_dotenv()
bot_token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(bot_token)
dp = Dispatcher(bot)

button_check_resp = KeyboardButton('Посмотреть расписание 📚', )
button_check_frined = KeyboardButton('Посмотреть сходства пар друзей 🤝')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(button_check_resp)
greet_kb.add(button_check_frined)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    
    await message.reply("Привет, я очень рад, что ты написал мне!\nЧто ты хочешь узнать на этот раз?", reply_markup=greet_kb)
    print(message.text)

@dp.message_handler()
async def process_messsage_command(message: types.Message):
    if message.text == "Посмотреть расписание 📚":
        await ask_full_name(message)
    elif message.text == 'Посмотреть сходства пар друзей 🤝':
        await ask_full_name(message)
    else:
        await message.reply(get_rasps(message.text))
    print(message.text)

async def ask_full_name(message):
    await message.reply('Напиши своё ФИО')




if __name__ == '__main__':
    executor.start_polling(dp)