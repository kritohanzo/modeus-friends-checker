import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv("DATABASE_NAME")

def connect_control(func: function) -> None:
    def wrapper(*args, **kwargs) -> None:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        func(cursor = cursor, *args, **kwargs)
        connection.commit()
        connection.close()
    return wrapper

@connect_control
def add_user(id: int, full_name: str, cursor: sqlite3.Cursor):
    cursor.execute(f"""INSERT INTO users (tg_id, full_name) VALUES ({id}, '{full_name}');""")

@connect_control
def delete_user(id: int, cursor: sqlite3.Cursor):
    cursor.execute(f"""DELETE FROM users WHERE tg_id = {id};""")

@connect_control
def update_user(id: int, full_name: str, cursor: sqlite3.Cursor):
    cursor.execute(f"""UPDATE users SET full_name = '{full_name}' WHERE tg_id = {id};""")

    
