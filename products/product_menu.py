import sqlite3
from repositories.category_repository import CategoryRepository

conn = sqlite3.connect('shop.db')
category_repo = CategoryRepository(conn)


def get_category_menu() -> None:
    categories = category_repo.get_all_categories()

    print("\nВыберите категорию товаров:")
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category[1]}")
    print("E. Выйти в главное меню")
