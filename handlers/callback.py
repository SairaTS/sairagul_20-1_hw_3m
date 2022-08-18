from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot


# @dp.callback_query_handler(lambda call: call.data == "button_call_1")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_2 = InlineKeyboardButton("NEXT", callback_data='button_call_2')
    markup.add(button_call_2)

    question = "В какой стране Эйнштейну предложили стать президентом?"
    answers = [
        "США",
        "Германия",
        "UK",
        "Франция",
        "Израиль"
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type="quiz",
        correct_option_id=4,
        open_period=10,
        reply_markup=markup
    )


# @dp.callback_query_handler(lambda call: call.data == "button_call_2")
async def quiz_3(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_3 = InlineKeyboardButton("NEXT", callback_data='button_call_3')
    markup.add(button_call_3)

    question = "В какой стране родился Эйнштейн?"
    answers = [
        "США",
        "Германия",
        "UK",
        "Франция",
        "Израиль"
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type="quiz",
        correct_option_id=1,
        open_period=10,
        reply_markup=markup
    )


# @config.dp.message_handler(commands=['mem'])
async def start_handler(message: types.Message):
    mem = open('media/sticker.webp', 'rb')
    await bot.send_sticker(message.chat.id, mem)


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
    dp.register_callback_query_handler(quiz_3, lambda call: call.data == "button_call_2")
    dp.register_message_handler(start_handler, commands=['mem'])
