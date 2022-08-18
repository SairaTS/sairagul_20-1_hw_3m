from aiogram.utils import executor
import config
from config import dp, bot
import logging
from handlers import client, callback, extra, admin, fsm_questionnaire

client.register_handlers_client(dp)
callback.register_handlers_callback(dp)
fsm_questionnaire.register_handlers_fsmquestionnaire(dp)
admin.register_handlers_admin(dp)

extra.register_handlers_extra(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
