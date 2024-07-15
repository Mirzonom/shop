from database import initialize_database
from get_catalog_guest import get_catalog_quest
from menu import MainChoice, show_main_menu
from user import register_user, login_user
from user_actions import handle_user_actions


def run_interface():
    initialize_database()

    print("Добро пожаловать в интернет-магазин")
    while True:
        choice = show_main_menu()

        if choice == MainChoice.REGISTER.value:
            username: str = input("Введите имя пользователя: ")
            password: str = input("Введите пароль: ")
            user: tuple = register_user(username, password)
            if user:
                user_id: int = user[0]
                handle_user_actions(user_id)

        elif choice == MainChoice.LOGIN.value:
            username: str = input("Введите имя пользователя: ")
            password: str = input("Введите пароль: ")
            user: tuple = login_user(username, password)
            if user:
                user_id: int = user[0]
                handle_user_actions(user_id)

        elif choice == MainChoice.GUEST_CATALOG.value:
            get_catalog_quest()

        elif choice == MainChoice.EXIT.value:
            print("Вы вышли с программы.")
            break

        else:
            print("Некорректный выбор.")
