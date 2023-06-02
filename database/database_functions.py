import os
import sqlite3

from dotenv import load_dotenv


load_dotenv()
db_name = os.getenv("DATABASE_NAME")


def connect_control(func) -> None:
    def wrapper(*args, **kwargs) -> None:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        result = func(cursor=cursor, *args, **kwargs)
        connection.commit()
        connection.close()
        return result

    return wrapper

@connect_control
def add_user(id: int, full_name: str, cursor: sqlite3.Cursor):
    cursor.execute(
        f"""INSERT INTO users (tg_id, full_name) VALUES ({id}, '{full_name}');"""
    )


@connect_control
def delete_user(id: int, cursor: sqlite3.Cursor):
    cursor.execute(f"""DELETE FROM users WHERE tg_id = {id};""")


@connect_control
def update_user(id: int, full_name: str, cursor: sqlite3.Cursor):
    cursor.execute(
        f"""UPDATE users SET full_name = '{full_name}' WHERE tg_id = {id};"""
    )


@connect_control
def check_user(id: int, cursor: sqlite3.Cursor):
    cursor.execute(f"""SELECT full_name FROM users WHERE tg_id = {id};""")
    cursor = cursor.fetchone()
    if cursor:
        return cursor[0]
    return False

@connect_control
def create_db(cursor: sqlite3.Cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(tg_id int, full_name char);""")

if __name__ == "__main__":
    create_db()
