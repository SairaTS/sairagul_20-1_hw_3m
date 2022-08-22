import sqlite3
from config import bot
import random


def sql_create():
    global db, cursor
    db = sqlite3.connect('bot.sqlite3')
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("CREATE TABLE IF NOT EXISTS menu "
               "(id INTEGER PRIMARY KEY, username TEXT, "
               "photo TEXT, name TEXT, description TEXT , "
               "price INTEGER)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy as data:
        cursor.execute("INSERT INTO questionnaire VALUES "
                       "(?, ?, ?, ?, ?, ?)",
                       tuple(data.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM questionnaire").fetchall()
    random_user = random.choice(result)
    await bot.send_photo(message.from_user.id, random_user[2],
                         caption=f"Name: {random_user[3]}\n"
                                 f"Description: {random_user[4]}\n"
                                 f"Price: {random_user[5]}\n\n"
                                 f"{random_user[1]}")

async def sql_command_all():
    return cursor.execute("SELECT * FROM questionnaire").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM questionnaire WHERE id == ?", (id,))
    db.commit()
