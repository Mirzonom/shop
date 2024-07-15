from enum import Enum

from cart import checkout, purchase_history, view_cart
from get_catalog_user import get_catalog_user


class UserAction(Enum):
    VIEW_CATALOG = '1'
    VIEW_CART = '2'
    CHECKOUT = '3'
    PURCHASE_HISTORY = '4'
    LOGOUT = 'e'


def handle_user_actions(user_id: int) -> None:
    while True:
        print("\nВыберите действие:")
        print("1. Просмотр каталога товаров")
        print("2. Просмотр корзины")
        print("3. Оплата")
        print("4. История покупок")
        print("E. Выход из аккаунта")
        action = input("Ваш выбор: ")

        if action == UserAction.VIEW_CATALOG.value:
            get_catalog_user(user_id)

        elif action == UserAction.VIEW_CART.value:
            view_cart(user_id)

        elif action == UserAction.CHECKOUT.value:
            checkout(user_id)

        elif action == UserAction.PURCHASE_HISTORY.value:
            purchase_history(user_id)

        elif action == UserAction.LOGOUT.value:
            break

        else:
            print("Некорректный выбор.")
