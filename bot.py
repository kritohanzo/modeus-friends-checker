import asyncio
import os

from aiogram import Bot, Dispatcher
from database.database_functions import create_db
from dotenv import load_dotenv
from handlers import singup, work


async def main():
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_TOKEN")
    bot = Bot(bot_token)
    dp = Dispatcher()

    dp.include_routers(singup.router)
    dp.include_routers(work.router)

    create_db()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
