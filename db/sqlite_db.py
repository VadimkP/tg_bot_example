import sqlite3 as sql


def sql_start():
    global base, cur
    base = sql.connect('sqlite/tg_bot.db')
    cur = base.cursor()
    if base:
        print('DB connect OK!')
        print('--------------')
    base.execute("""CREATE TABLE IF NOT EXISTS honey(img TEXT, type TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)""")
    base.execute("""CREATE TABLE IF NOT EXISTS users(user_id TEXT UNIQUE, full_name TEXT)""")
    base.execute("""CREATE TABLE IF NOT EXISTS cart(name TEXT, user_id TEXT)""")
    base.commit()


async def users_stats(user_id, fn):
    cur.execute("""INSERT INTO users (user_id, full_name) VALUES (?, ?)""", (user_id, fn))
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO honey VALUES (?, ?, ?, ?, ?)""", tuple(data.values()))
        base.commit()


async def sql_read_honey():
    return cur.execute("""SELECT * FROM honey WHERE type="Мёд";""").fetchall()


async def sql_read_honeycomb():
    return cur.execute("""SELECT * FROM honey WHERE type="Соты";""").fetchall()


async def sql_read_tea():
    return cur.execute("""SELECT * FROM honey WHERE type="Чай";""").fetchall()


async def sql_read_tableware():
    return cur.execute("""SELECT * FROM honey WHERE type="Посуда";""").fetchall()


async def sql_read_other():
    return cur.execute("""SELECT * FROM honey WHERE type="Другое";""").fetchall()


async def sql_read2():
    return cur.execute("""SELECT * FROM honey""").fetchall()


async def sql_delete_command(data):
    cur.execute("""DELETE FROM honey WHERE name == ?""", (data,))
    base.commit()


async def sql_users():
    return cur.execute("""SELECT * FROM users""").fetchall()


async def sql_add_cart(name, user_id):
    cur.execute("""INSERT INTO cart VALUES (?, ?)""", (name, user_id))
    base.commit()


async def sql_read_cart(user):
    return cur.execute("""SELECT cart.name, honey.price FROM cart, honey WHERE cart.name == honey.name AND
      cart.user_id = ?""", (user,)).fetchall()


async def sql_del_one_pos_from_cart(data, user):
    cur.execute("""DELETE FROM cart WHERE name == ? and user_id == ?""", (data, user))
    base.commit()


async def sql_del_all_user_cart(user):
    cur.execute("""DELETE FROM cart WHERE user_id == ?""", (user,))
    base.commit()

