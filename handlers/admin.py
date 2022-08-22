from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot
from config import ADMIN
import random


async def game(message: types.Message):
    if message.text.startswith('game'):
        if message.from_user.id in ADMIN:
            emoji_list = ['🏀', '🎯', '🎳', '🎰', '⚽️']
            emoji = random.choice(emoji_list)
            await bot.send_dice(message.chat.id, emoji=emoji)
        else:
            await message.reply("Вы не админ!!!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(game)
