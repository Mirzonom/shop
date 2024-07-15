import sqlite3
from typing import Optional, Tuple, List, Any


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self) -> None:
        sql_query(self.conn, '''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )
                ''')

    def create_user(self, username: str, password: str) -> int:
        return sql_query(self.conn, '''
                        INSERT INTO users (username, password) VALUES (?, ?)
                    ''', (username, password), return_type='lastrowid')

    def find_by_username(self, username: str) -> Optional[tuple]:
        return sql_query(self.conn, '''
                        SELECT * FROM users WHERE username = ?
                    ''', (username,), return_type='fetchone')

    def get_virtual_balance(self, user_id: int) -> float:
        transactions = sql_query(self.conn, "SELECT amount, type FROM money_transactions WHERE user_id = ?",
                                 (user_id,), return_type='fetchall')
        total_balance = 1000.0  # начальный баланс
        for amount, transaction_type in transactions:
            if transaction_type == 0:  # списание
                total_balance -= amount
            elif transaction_type == 1:  # зачисление
                total_balance += amount
        return total_balance

    def delete_user(self, user_id: int) -> None:
        sql_query(self.conn, '''
                DELETE FROM users WHERE id = ?
            ''', (user_id,))


class TransactionRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_table_money_transaction(self) -> None:
        sql_query(self.conn, '''
                    CREATE TABLE IF NOT EXISTS money_transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        amount REAL NOT NULL,
                        type INTEGER NOT NULL, -- 0 для списания, 1 для зачисления
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')

    def create_table_quantity_transaction(self) -> None:
        sql_query(self.conn, '''
                            CREATE TABLE IF NOT EXISTS product_transactions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                product_id INTEGER NOT NULL,
                                quantity INTEGER NOT NULL,
                                type INTEGER NOT NULL, -- 0 для списания, 1 для зачисления
                                FOREIGN KEY (product_id) REFERENCES products(id)
                            )
                        ''')

    def add_money_transaction(self, user_id: int, amount: float, transaction_type: int) -> None:
        sql_query(self.conn, '''
            INSERT INTO money_transactions (user_id, amount, type) VALUES (?, ?, ?)
        ''', (user_id, amount, transaction_type))

    def add_product_quantity_transaction(self, product_id: int, quantity: int, transaction_type: int) -> None:
        sql_query(self.conn, '''
            INSERT INTO product_transactions (product_id, quantity, type) VALUES (?, ?, ?)
        ''', (product_id, quantity, transaction_type))


class CategoryRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self) -> None:
        sql_query(self.conn, '''
                        CREATE TABLE IF NOT EXISTS categories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL UNIQUE
                        )
                    ''')

    def create_category(self, name: str) -> int:
        return sql_query(self.conn, '''
            INSERT INTO categories (name) VALUES (?)
            ''', (name,), return_type='lastrowid')

    def find_by_name(self, name: str) -> Optional[tuple]:
        return sql_query(self.conn, '''
                SELECT * FROM categories WHERE name = ?
                    ''', (name,), return_type='fetchone')

    def get_all_categories(self) -> List[Tuple[int, str]]:
        return sql_query(self.conn, 'SELECT id, name FROM categories', return_type='fetchall')


class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self) -> None:
        sql_query(self.conn, '''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        category_id INTEGER NOT NULL,
                        stock INTEGER DEFAULT 0,
                        FOREIGN KEY (category_id) REFERENCES categories(id)
                    )
                ''')

    def create_product(self, name: str, price: float, category_id: int, stock: int) -> int:
        return sql_query(self.conn, '''
            INSERT INTO products (name, price, category_id, stock) VALUES (?, ?, ?, ?)
            ''', (name, price, category_id, stock), return_type='lastrowid')

    def find_by_id(self, product_id: int) -> Optional[tuple]:
        return sql_query(self.conn, '''
            SELECT * FROM products WHERE id = ?
            ''', (product_id,), return_type='fetchone')

    def find_by_name(self, name: str) -> Optional[tuple]:
        return sql_query(self.conn, '''
            SELECT * FROM products WHERE name = ?
        ''', (name,), return_type='fetchone')

    def get_products_by_category(self, category_name: str) -> List[Tuple[int, str, float, int]]:
        return sql_query(self.conn, '''
                SELECT products.id, products.name, products.price, products.stock
                FROM products
                JOIN categories ON products.category_id = categories.id
                WHERE categories.name = ? AND products.stock > 0
            ''', (category_name,), return_type='fetchall')

    def get_products_by_category_id(self, category_id) -> List[Tuple[int, str, float, int]]:
        return sql_query(self.conn, '''
                SELECT id, name, price, stock
                FROM products
                WHERE category_id = ? AND stock > 0
            ''', (category_id,), return_type='fetchall')

    def update_stock(self, product_id: int, new_stock: int, transaction_type: int) -> None:
        sql_query(self.conn, '''
            UPDATE products SET stock = ? WHERE id = ?
            ''', (new_stock, product_id))

    def get_virtual_product_quantity(self, product_id: int) -> int:
        transactions = sql_query(self.conn, "SELECT quantity, type FROM product_transactions WHERE product_id = ?",
                                 (product_id,), return_type='fetchall')
        total_quantity = self.find_by_id(product_id)[4]  # исходный stock из таблицы products
        for quantity, transaction_type in transactions:
            if transaction_type == 0:  # списание
                total_quantity -= quantity
            elif transaction_type == 1:  # зачисление
                total_quantity += quantity
        return total_quantity


class OrderRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self) -> None:
        sql_query(self.conn, '''
                        CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            product_id INTEGER NOT NULL,
                            quantity INTEGER NOT NULL,
                            total_price REAL NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            status TEXT DEFAULT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(id),
                            FOREIGN KEY (product_id) REFERENCES products(id)
                        )
                    ''')

    def create_order(self, user_id: int, product_id: int, quantity: int, total_price: float) -> int:
        return sql_query(self.conn, '''
            INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?)
            ''', (user_id, product_id, quantity, total_price), return_type='lastrowid')

    def find_by_user(self, user_id: int) -> list:
        return sql_query(self.conn, '''
            SELECT * FROM users WHERE id = ?
            ''', (user_id,), return_type='fetchall')

    def check_my_orders_by_user_id(self, user_id: int) -> List[Tuple[int, str]]:
        return sql_query(self.conn, 'SELECT * FROM orders WHERE user_id=? AND status IS NULL',
                         (user_id,), return_type='fetchall')

    def view_orders_from_cart(self, user_id: int) -> List[Tuple[str, int, float]]:
        return sql_query(self.conn, '''
            SELECT products.name, orders.quantity, orders.total_price
            FROM orders
            INNER JOIN products ON orders.product_id = products.id
            WHERE orders.user_id = ? AND orders.status IS NULL
            ''', (user_id,), return_type='fetchall')

    def get_completed_orders(self, user_id: int) -> List[Tuple[str, int, float, str]]:
        return sql_query(self.conn, '''
            SELECT products.name, orders.quantity, orders.total_price, orders.timestamp
            FROM orders
            INNER JOIN products ON orders.product_id = products.id
            WHERE orders.user_id = ? AND orders.status = 'completed'
            ''', (user_id,), return_type='fetchall')

    def update_status(self, order_id: int, status: str) -> None:
        sql_query(self.conn, '''UPDATE orders SET status = ? WHERE id = ?''', (status, order_id))

    def delete_orders_with_null_status(self) -> None:
        sql_query(self.conn, '''DELETE FROM orders WHERE status IS NULL''')


def initialize_database() -> None:
    conn = sqlite3.connect('shop.db')
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

        # categories = ['Блокноты', 'Ручки', 'Карандаши', 'Пеналы', 'Линейки']
        # for category in categories:
        #     if not category_repo.find_by_name(category):
        #         category_repo.create_category(category)
        #
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
        #     ('Prismacolor карандаш', 1.79, 3, 0),
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
        #
        # for product in products:
        #     name, price, category_id, stock = product
        #     if not product_repo.find_by_name(name):
        #         product_id = product_repo.create_product(name, price, category_id, stock)
        #         transaction_repo.add_product_quantity_transaction(product_id, stock, 1)

    finally:
        close_database(conn)


def close_database(conn) -> None:
    conn.close()


def sql_query(conn, query: str, params: tuple = (), return_type: str = 'lastrowid') -> Any:
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, params)

        if return_type == 'fetchall':
            return cursor.fetchall()
        elif return_type == 'fetchone':
            return cursor.fetchone()
        return cursor.lastrowid
