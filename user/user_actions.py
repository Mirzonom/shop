from enum import Enum
import sqlite3

from catalogs.get_catalog_user import get_catalog_user
from services.view_cart_service import ViewCartService
from services.checkout_service import CheckoutService
from services.purchase_history_service import PurchaseHistoryService

conn = sqlite3.connect('shop.db')
view_cart_service = ViewCartService(conn)
checkout_service = CheckoutService(conn)
purchase_history_service = PurchaseHistoryService(conn)


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
        action = input("Ваш выбор: ").lower()

        if action == UserAction.VIEW_CATALOG.value:
            get_catalog_user(user_id)

        elif action == UserAction.VIEW_CART.value:
            view_cart_service.view_cart(user_id)

        elif action == UserAction.CHECKOUT.value:
            checkout_service.checkout(user_id)

        elif action == UserAction.PURCHASE_HISTORY.value:
            purchase_history_service.purchase_history(user_id)

        elif action == UserAction.LOGOUT.value:
            break

        else:
            print("Некорректный выбор.")
