import sqlite3 as sql
from create_bot import bot


def sql_start():
    global base, cur
    base = sql.connect('sqlite/tg_bot.db')
    cur = base.cursor()
    if base:
        print('DB connect OK!')
    base.execute('CREATE TABLE IF NOT EXISTS honey(img TEXT, type TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT UNIQUE, full_name TEXT)')
    base.commit()


async def order(user_id, fn):
    cur.execute('INSERT INTO users (user_id, full_name) VALUES (?, ?)', (user_id, fn))
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO honey VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read_honey():
    return cur.execute('SELECT * FROM honey WHERE type="Мёд";').fetchall()


async def sql_read_honeycomb():
    return cur.execute('SELECT * FROM honey WHERE type="Соты";').fetchall()


async def sql_read_tea():
    return cur.execute('SELECT * FROM honey WHERE type="Чай";').fetchall()


async def sql_read_tableware():
    return cur.execute('SELECT * FROM honey WHERE type="Посуда";').fetchall()


async def sql_read_other():
    return cur.execute('SELECT * FROM honey WHERE type="Другое";').fetchall()


async def sql_read2():
    return cur.execute('SELECT * FROM honey').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM honey WHERE name == ?', (data,))
    base.commit()


async def sql_users():
    return cur.execute('SELECT * FROM users').fetchall()

