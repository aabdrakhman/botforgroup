"""This is BotForGroup"""

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentTypes, Message

import os
from dotenv import load_dotenv
load_dotenv()

from sqlite_db import DBHelper
db = DBHelper()

import asyncio
import aioschedule

API_TOKEN = str(os.getenv("API_TOKEN"))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm BotForGroup!")



@dp.message_handler()
async def get_message(message: types.Message):
    db.insert_message(message)



@dp.message_handler()
async def send_message():
    await bot.send_message(-759201949, 'Какие результаты за сегодняшний день?)')


  
@dp.message_handler()
async def send_warning_message():
    if len(db.warning_message()):
        await bot.send_message(-759201949, ' , '.join(db.warning_message())+' За неделю от вас не было сообщений')
    
    
    
async def scheduler():
    aioschedule.every().day.at("18:47").do(send_warning_message)
    aioschedule.every().day.at("05:00").do(kick_member)
    aioschedule.every().day.at("17:00").do(send_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



async def on_startup(dp): 
    asyncio.create_task(scheduler())


 
@dp.message_handler()
async def kick_member():
    if len(db.kick_member_query()):
        for i in db.kick_member_query():
            await bot.kick_chat_member(-759201949, i)


   
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True,  on_startup=on_startup)
