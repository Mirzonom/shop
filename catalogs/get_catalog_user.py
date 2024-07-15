import sqlite3
from typing import List

from products.product_display import show_products
from products.product_menu import get_category_menu
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository

conn = sqlite3.connect('shop.db')
category_repo = CategoryRepository(conn)
product_repo = ProductRepository(conn)


def get_catalog_user(user_id) -> None:
    while True:
        categories: List[tuple] = category_repo.get_all_categories()

        get_category_menu()

        category_choice: str = input("Ваш выбор: ").lower()

        if category_choice.isdigit():
            category_choice: int = int(category_choice)
            if 1 <= category_choice <= len(categories):
                category_id: int = categories[category_choice - 1][0]
                show_products(category_id, user_id)
            elif category_choice == len(categories) + 1:
                break
            else:
                print("Некорректный выбор.")

        elif category_choice == 'e':
            break

        else:
            print("Некорректный выбор.")
