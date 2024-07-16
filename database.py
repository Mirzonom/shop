import sqlite3

from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository


def initialize_database() -> None:
    conn = sqlite3.connect('shop.db')
    conn.execute('PRAGMA foreign_keys = ON')
    try:

        user_repo = UserRepository(conn)
        user_repo.create_table()

        transaction_repo = TransactionRepository(conn)
        transaction_repo.create_table_money_transaction()
        transaction_repo.create_table_quantity_transaction()

        category_repo = CategoryRepository(conn)
        category_repo.create_table()

        product_repo = ProductRepository(conn)
        product_repo.create_table()

        order_repo = OrderRepository(conn)
        order_repo.create_table()

        # user_repo.delete_user(user_id=2)

        # categories = ['Блокноты', 'Ручки', 'Карандаши', 'Пеналы', 'Линейки']
        # for category in categories:
        #     if not category_repo.find_by_name(category):
        #         category_repo.create_category(category)

        # products = [
        #     ('Moleskine блокнот', 12.99, 1, 8),
        #     ('Leuchtturm1917 блокнот', 17.95, 1, 15),
        #     ('Field Notes блокнот', 9.95, 1, 3),
        #     ('Rhodia блокнот', 8.50, 1, 17),
        #     ('Artline блокнот', 4.95, 1, 5),
        #     ('Stabilo блокнот', 2.79, 1, 10),
        #     ('Sharpie блокнот', 1.99, 1, 16),
        #     ('Pilot блокнот', 3.79, 1, 7),
        #     ('Copic блокнот', 7.99, 1, 15),
        #     ('Parker ручка', 24.99, 2, 10),
        #     ('Pilot ручка', 7.49, 2, 18),
        #     ('Lamy ручка', 29.99, 2, 5),
        #     ('Faber-Castell карандаш', 1.99, 3, 12),
        #     ('Prismacolor карандаш', 1.79, 3, 10),
        #     ('Koh-I-Noor карандаш', 2.49, 3, 7),
        #     ('Derwent пенал', 14.99, 4, 6),
        #     ('Easthill пенал', 10.99, 4, 9),
        #     ('Kipling пенал', 19.95, 4, 4),
        #     ('Westcott линейка', 2.99, 5, 11),
        #     ('Maped линейка', 1.49, 5, 2),
        #     ('Staedtler линейка', 3.99, 5, 13),
        #     ('Cross ручка', 39.99, 2, 3),
        #     ('Tombow карандаш', 3.29, 3, 8),
        #     ('Zebra гелевая ручка', 6.99, 2, 14),
        #     ('Uni-ball карандаш', 2.19, 3, 13),
        #     ('Pentel ручка', 5.49, 2, 19),
        #     ('Pentel карандаш', 4.49, 3, 18),
        #     ('Staedtler пенал', 11.49, 4, 10),
        #     ('Faber-Castell ручка', 8.99, 2, 20),
        #     ('Pilot гелевая ручка', 4.59, 2, 6)
        # ]

        # for product in products:
        #     name, price, category_id, stock = product
        #     if not product_repo.find_by_name(name):
        #         product_id = product_repo.create_product(
        #             name, price, category_id, stock)
        #         transaction_repo.add_product_quantity_transaction(
        #             product_id, stock, 1)

    finally:
        close_database(conn)


def close_database(conn) -> None:
    conn.close()


def set_foreign_keys(self):
    self.conn.execute("PRAGMA FOREIGN_KEYS = ON")
