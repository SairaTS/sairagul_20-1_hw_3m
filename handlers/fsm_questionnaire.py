from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot
from keyboards.client_kb import cancel_markup
from database import bot_db


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdmin.photo.set()
        await message.answer(f"Hi {message.from_user.full_name}" f" send photo...",
                             reply_markup=cancel_markup)
    else:
        await message.reply("Write DM!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[id] = message.from_user.id
        data['username'] = f"@{message.from_user.username}"
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("How is that food called?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("What kind of ingredients are used? ")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.answer("How much does it cost?")


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        valid = False
        while not valid:
            data['price'] = message.text
            if type(int(data['price'])) is int:
                await message.answer(data['price'])
                valid = True
            else:
                await message.reply("only integers")

        await bot.send_photo(message.from_user.id, data['photo'],
                             caption=f"Name: {data['name']}\n"
                                     f"Description: {data['description']}\n"
                                     f"Price: {data['price']}\n\n"
                                     f"{data['username']}")
    await bot_db.sql_command_insert(state)
    await state.finish()
    await message.answer("That is the end, thank you for your time)")


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer("Registration is cancelled!")


async def delete_data(message: types.Message):
    if message.from_user.id in ADMIN and message.chat.type == "private":
        users = await bot_db.sql_command_all()
        for user in users:
            await bot.send_photo(message.from_user.id, random_user[2],
                                 caption=f"Name: {random_user[3]}\n"
                                         f"Description: {random_user[4]}\n"
                                         f"Price: {random_user[5]}\n\n"
                                         f"{random_user[1]}"
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(
                                         f"delete: {user[3]}",
                                         callback_data=f"delete{user[0]}"
                                     )
                                 )
                                 )

    else:
        await message.reply("You are not ADMIN!")

async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace('delete ', ""))
    await call.answer(text="Deleted from DB", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_handlers_fsmquestionnaire(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands='cancel')
    dp.register_message_handler(cancel_registration, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(
        complete_delete,
        lambda call: call.data and call.data.startswith("delete ")
    )
