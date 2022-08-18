from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot
import random


# @dp.message_handler()
async def echo(message: types.Message):
    x = message.text
    try:
        x = int(x)
        c = 1
    except:
        pass
        c = 0
    if c == 1:
        await bot.send_message(message.chat.id, f'{x ** 2}')
    elif c == 0:
        await bot.send_message(message.chat.id, x)
    else:
        pass


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(echo)

