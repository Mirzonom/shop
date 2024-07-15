import hashlib
import sqlite3
from typing import Optional

from database import UserRepository

conn = sqlite3.connect('shop.db')
user_repo = UserRepository(conn)


def register_user(username: str, password: str) -> Optional[tuple]:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        user_repo.create_user(username, hashed_password)
        print("Регистрация успешна.")
        return user_repo.find_by_username(username)
    except sqlite3.IntegrityError:
        print("Пользователь с таким именем уже существует.")


def login_user(username: str, password: str) -> Optional[tuple]:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = user_repo.find_by_username(username)
    if user and user[2] == hashed_password:
        print("Вход выполнен успешно.")
        return user
    else:
        print("Неправильное имя пользователя или пароль.")
        return None
