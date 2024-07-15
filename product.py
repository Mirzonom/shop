import sqlite3
from typing import Optional

from cart import add_to_cart
from database import ProductRepository, CategoryRepository

conn = sqlite3.connect('shop.db')
product_repo = ProductRepository(conn)
category_repo = CategoryRepository(conn)


def get_products_by_category(category_name):
    return product_repo.get_products_by_category(category_name)


def show_products(category_id: int, user_id: Optional[int] = None):
    if user_id is not None:
        while True:
            products = product_repo.get_products_by_category_id(category_id)
            if products:
                print("\nДоступные товары:")
                for index, product in enumerate(products, start=1):
                    print(f"{index}. {product[1]} - ${product[2]}.")

                product_index = input(
                    "Введите ID товара для добавления в корзину (или 'E' для выхода): ")
                if product_index.lower() == 'e':
                    break
                else:
                    product_index = int(product_index) - 1
                    if 0 <= product_index < len(products):
                        product_id = products[product_index][0]
                        quantity = int(input("Введите количество: "))
                        add_to_cart(user_id, product_id, quantity)
                    else:
                        print("Некорректное номер товара.")
            else:
                print("Нет товаров в данной категории.")
                break

    else:
        while True:
            products = product_repo.get_products_by_category_id(category_id)
            if products:
                print("\nДоступные товары:")
                for product in products:
                    print(f"{product[1]} - ${product[2]}.")
            else:
                print("Нет товаров в данной категории.")

            exit_choice = input("Введите 'E' для выхода назад: ")
            if exit_choice.lower() == 'e':
                break


def get_category_menu() -> None:
    categories = category_repo.get_all_categories()

    print("\nВыберите категорию товаров:")
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category[1]}")
    print("E. Выйти в главное меню")
