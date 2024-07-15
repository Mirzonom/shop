import sqlite3
from typing import List

from database import ProductRepository, CategoryRepository
from product import show_products, get_category_menu

conn = sqlite3.connect('shop.db')
category_repo = CategoryRepository(conn)
product_repo = ProductRepository(conn)


def get_catalog_quest() -> None:
    while True:
        categories: List[tuple] = category_repo.get_all_categories()

        get_category_menu()

        category_choice: str = input("Ваш выбор: ")

        if category_choice.isdigit():
            category_index: int = int(category_choice) - 1
            if 0 <= category_index < len(categories):
                category_id: int = categories[category_index][0]
                show_products(category_id)  # без user_id, так как это режим гостья
            else:
                print("Некорректный выбор.")
        elif category_choice == 'e':
            break
        else:
            print("Некорректный выбор.")
