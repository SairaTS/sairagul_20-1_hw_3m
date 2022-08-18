from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot
from keyboards.client_kb import cancel_markup


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
    await state.finish()
    await message.answer("That is the end, thank you for your time)")


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer("Registration is cancelled!")


def register_handlers_fsmquestionnaire(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands='cancel')
    dp.register_message_handler(cancel_registration, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
