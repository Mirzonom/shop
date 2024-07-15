from enum import Enum
from typing import Optional


class MainChoice(Enum):
    REGISTER = '1'
    LOGIN = '2'
    GUEST_CATALOG = '3'
    EXIT = 'e'


def show_main_menu() -> Optional[str]:
    print("\nВыберите действие:")
    print("1. Регистрация")
    print("2. Вход")
    print("3. Просмотр товаров (как гость)")
    print("E. Выход")
    return input("Ваш выбор: ").lower()
